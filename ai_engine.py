"""
AI Engine for processing context and generating intelligent suggestions
"""

import openai
import json
import time
import threading
from typing import Dict, List, Optional, Any
import logging
from config import Config

class AIEngine:
    def __init__(self):
        self.client = None
        self.is_initialized = False
        self.logger = logging.getLogger(__name__)
        self.suggestion_cache = {}
        self.last_request_time = 0
        self.rate_limit_delay = 1.0  # seconds between requests
        
        # Initialize OpenAI client
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            if Config.OPENAI_API_KEY:
                openai.api_key = Config.OPENAI_API_KEY
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                self.is_initialized = True
                self.logger.info("AI Engine initialized successfully")
            else:
                self.logger.error("OpenAI API key not found in configuration")
        except Exception as e:
            self.logger.error(f"Error initializing AI Engine: {e}")
    
    def generate_suggestions(self, context: Dict, command: str = None, query: str = None) -> Dict:
        """Generate AI-powered suggestions based on context"""
        if not self.is_initialized:
            return {"error": "AI Engine not initialized"}
        
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_request_time < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay - (current_time - self.last_request_time))
            
            # Prepare prompt based on context and command
            prompt = self._build_prompt(context, command, query)
            
            # Generate response
            response = self._call_openai(prompt)
            
            # Parse and format response
            suggestions = self._parse_response(response, context)
            
            self.last_request_time = time.time()
            return suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating suggestions: {e}")
            return {"error": str(e)}
    
    def _build_prompt(self, context: Dict, command: str = None, query: str = None) -> str:
        """Build prompt for AI based on context and command"""
        prompt_parts = []
        
        # Base system prompt
        system_prompt = """You are an intelligent coding assistant that provides real-time help to developers. 
        Analyze the current context and provide relevant, actionable suggestions.
        
        Focus on:
        - Code quality and best practices
        - Error detection and fixes
        - Performance optimization
        - Security considerations
        - Modern development patterns
        
        Provide concise, practical suggestions that can be immediately applied."""
        
        prompt_parts.append(system_prompt)
        
        # Add context information
        if context.get("code_detected"):
            prompt_parts.append(f"\nLanguage: {context.get('language', 'Unknown')}")
            prompt_parts.append(f"File type: {context.get('file_type', 'Unknown')}")
        
        if context.get("error_indicators"):
            prompt_parts.append(f"Error indicators detected: {', '.join(context['error_indicators'])}")
        
        if context.get("suggestions_context"):
            prompt_parts.append(f"Context: {context['suggestions_context']}")
        
        # Add specific command or query
        if command:
            command_description = Config.VOICE_COMMANDS.get(command, command)
            prompt_parts.append(f"\nUser request: {command_description}")
        
        if query:
            prompt_parts.append(f"\nUser query: {query}")
        
        # Add code snippets if available
        if context.get("code_snippets"):
            prompt_parts.append("\nCode snippets detected:")
            for i, snippet in enumerate(context["code_snippets"][:3], 1):
                prompt_parts.append(f"Snippet {i}: {snippet}")
        
        # Add text content if available
        if context.get("text_content"):
            recent_text = context["text_content"][-1000:]  # Last 1000 characters
            prompt_parts.append(f"\nRecent screen content: {recent_text}")
        
        # Request specific output format
        prompt_parts.append("""
        Please provide your response in the following JSON format:
        {
            "suggestions": [
                {
                    "type": "code_fix|optimization|best_practice|security|documentation",
                    "title": "Brief title",
                    "description": "Detailed description",
                    "code": "Code snippet if applicable",
                    "priority": "high|medium|low"
                }
            ],
            "summary": "Brief summary of main issues/suggestions",
            "confidence": 0.0-1.0
        }
        """)
        
        return "\n".join(prompt_parts)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    def _parse_response(self, response: str, context: Dict) -> Dict:
        """Parse AI response and format suggestions"""
        try:
            # Try to parse JSON response
            if response.strip().startswith("{"):
                parsed = json.loads(response)
                return self._format_suggestions(parsed, context)
            else:
                # Fallback: treat as plain text
                return self._format_text_response(response, context)
                
        except json.JSONDecodeError:
            self.logger.warning("Could not parse JSON response, treating as text")
            return self._format_text_response(response, context)
        except Exception as e:
            self.logger.error(f"Error parsing response: {e}")
            return {"error": "Failed to parse AI response"}
    
    def _format_suggestions(self, parsed: Dict, context: Dict) -> Dict:
        """Format parsed suggestions"""
        suggestions = {
            "timestamp": time.time(),
            "context": context,
            "suggestions": parsed.get("suggestions", []),
            "summary": parsed.get("summary", ""),
            "confidence": parsed.get("confidence", 0.5),
            "source": "ai_engine"
        }
        
        # Validate and clean suggestions
        valid_suggestions = []
        for suggestion in suggestions["suggestions"]:
            if isinstance(suggestion, dict) and "title" in suggestion:
                valid_suggestion = {
                    "type": suggestion.get("type", "general"),
                    "title": suggestion.get("title", ""),
                    "description": suggestion.get("description", ""),
                    "code": suggestion.get("code", ""),
                    "priority": suggestion.get("priority", "medium")
                }
                valid_suggestions.append(valid_suggestion)
        
        suggestions["suggestions"] = valid_suggestions
        return suggestions
    
    def _format_text_response(self, response: str, context: Dict) -> Dict:
        """Format plain text response as suggestions"""
        return {
            "timestamp": time.time(),
            "context": context,
            "suggestions": [
                {
                    "type": "general",
                    "title": "AI Suggestion",
                    "description": response,
                    "code": "",
                    "priority": "medium"
                }
            ],
            "summary": response[:200] + "..." if len(response) > 200 else response,
            "confidence": 0.5,
            "source": "ai_engine"
        }
    
    def analyze_code_quality(self, code_snippet: str, language: str = None) -> Dict:
        """Analyze code quality and provide suggestions"""
        if not self.is_initialized:
            return {"error": "AI Engine not initialized"}
        
        try:
            prompt = f"""
            Analyze the following {language or 'code'} for quality issues:
            
            {code_snippet}
            
            Provide analysis in JSON format:
            {{
                "issues": [
                    {{
                        "type": "syntax|logic|performance|security|style",
                        "severity": "high|medium|low",
                        "description": "Issue description",
                        "suggestion": "How to fix"
                    }}
                ],
                "score": 0.0-1.0,
                "improvements": ["list of improvements"]
            }}
            """
            
            response = self._call_openai(prompt)
            return json.loads(response)
            
        except Exception as e:
            self.logger.error(f"Error analyzing code quality: {e}")
            return {"error": str(e)}
    
    def suggest_fixes(self, error_message: str, code_context: str = None) -> Dict:
        """Suggest fixes for errors"""
        if not self.is_initialized:
            return {"error": "AI Engine not initialized"}
        
        try:
            prompt = f"""
            Suggest fixes for this error:
            
            Error: {error_message}
            
            Code context: {code_context or 'Not provided'}
            
            Provide fixes in JSON format:
            {{
                "fixes": [
                    {{
                        "description": "Fix description",
                        "code": "Fixed code",
                        "explanation": "Why this fixes the issue"
                    }}
                ],
                "prevention": "How to prevent this error in the future"
            }}
            """
            
            response = self._call_openai(prompt)
            return json.loads(response)
            
        except Exception as e:
            self.logger.error(f"Error suggesting fixes: {e}")
            return {"error": str(e)}
    
    def generate_documentation(self, code_snippet: str, language: str = None) -> Dict:
        """Generate documentation for code"""
        if not self.is_initialized:
            return {"error": "AI Engine not initialized"}
        
        try:
            prompt = f"""
            Generate documentation for this {language or 'code'}:
            
            {code_snippet}
            
            Provide documentation in JSON format:
            {{
                "description": "Function/class description",
                "parameters": ["parameter descriptions"],
                "returns": "Return value description",
                "examples": ["usage examples"],
                "notes": "Additional notes"
            }}
            """
            
            response = self._call_openai(prompt)
            return json.loads(response)
            
        except Exception as e:
            self.logger.error(f"Error generating documentation: {e}")
            return {"error": str(e)}
    
    def get_cached_suggestion(self, context_hash: str) -> Optional[Dict]:
        """Get cached suggestion if available"""
        if Config.ENABLE_CACHING and context_hash in self.suggestion_cache:
            cached = self.suggestion_cache[context_hash]
            if time.time() - cached["timestamp"] < Config.CACHE_TTL:
                return cached["suggestion"]
        return None
    
    def cache_suggestion(self, context_hash: str, suggestion: Dict):
        """Cache suggestion for future use"""
        if Config.ENABLE_CACHING:
            self.suggestion_cache[context_hash] = {
                "timestamp": time.time(),
                "suggestion": suggestion
            }
    
    def clear_cache(self):
        """Clear suggestion cache"""
        self.suggestion_cache.clear()
        self.logger.info("Suggestion cache cleared") 