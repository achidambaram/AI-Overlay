#!/usr/bin/env python3
"""
Open Source LLM Copilot
Uses free, open source language models instead of OpenAI API
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import json
import requests
import subprocess
import os
from typing import Dict, List, Optional
import logging

class OpenSourceCopilot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Open Source LLM Copilot")
        self.root.geometry("800x600")
        
        # LLM providers
        self.llm_providers = {
            "ollama": {
                "name": "Ollama (Local)",
                "description": "Run LLMs locally on your machine",
                "models": ["codellama", "llama2", "mistral", "gemma"],
                "setup_required": True
            },
            "huggingface": {
                "name": "Hugging Face (Free)",
                "description": "Use free models from Hugging Face",
                "models": ["microsoft/DialoGPT-medium", "gpt2", "distilgpt2"],
                "setup_required": False
            },
            "local_transformers": {
                "name": "Local Transformers",
                "description": "Download and run models locally",
                "models": ["gpt2", "distilgpt2", "microsoft/DialoGPT-medium"],
                "setup_required": True
            }
        }
        
        self.current_provider = "ollama"
        self.current_model = "codellama"
        self.is_connected = False
        
        # Demo contexts
        self.demo_contexts = [
            {
                "code_detected": True,
                "language": "python",
                "file_type": ".py",
                "error_indicators": ["SyntaxError", "IndentationError"],
                "suggestions_context": "Python code with syntax errors detected",
                "code_snippets": [
                    "def calculate_sum(a, b:\n    return a + b",
                    "if x > 0\n    print('Positive')",
                    "for i in range(10)\n    print(i)"
                ]
            },
            {
                "code_detected": True,
                "language": "javascript",
                "file_type": ".js",
                "error_indicators": ["ReferenceError", "TypeError"],
                "suggestions_context": "JavaScript code with reference errors",
                "code_snippets": [
                    "console.log(undefinedVariable);",
                    "const result = someFunction();",
                    "let arr = [1, 2, 3];\narr.push(4);"
                ]
            },
            {
                "code_detected": True,
                "language": "html",
                "file_type": ".html",
                "error_indicators": ["ValidationError"],
                "suggestions_context": "HTML with validation issues",
                "code_snippets": [
                    "<div>\n    <p>Unclosed paragraph\n</div>",
                    "<img src='image.jpg'>",
                    "<script>\n    console.log('Hello');\n</script>"
                ]
            }
        ]
        
        self.current_context_index = 0
        self.demo_suggestions = []
        
        self.setup_ui()
        self.check_llm_availability()
        
    def check_ollama_availability(self) -> bool:
        """Check if Ollama is installed and running"""
        try:
            # Check if ollama command exists
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def check_ollama_models(self) -> List[str]:
        """Get available Ollama models"""
        try:
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []
    
    def check_huggingface_availability(self) -> bool:
        """Check if Hugging Face is accessible"""
        try:
            response = requests.get("https://huggingface.co/api/models", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def check_llm_availability(self):
        """Check availability of different LLM providers"""
        self.llm_status = {}
        
        # Check Ollama
        ollama_available = self.check_ollama_availability()
        self.llm_status["ollama"] = {
            "available": ollama_available,
            "models": self.check_ollama_models() if ollama_available else []
        }
        
        # Check Hugging Face
        hf_available = self.check_huggingface_availability()
        self.llm_status["huggingface"] = {
            "available": hf_available,
            "models": self.llm_providers["huggingface"]["models"]
        }
        
        # Check local transformers
        try:
            import transformers
            self.llm_status["local_transformers"] = {
                "available": True,
                "models": self.llm_providers["local_transformers"]["models"]
            }
        except ImportError:
            self.llm_status["local_transformers"] = {
                "available": False,
                "models": []
            }
    
    def query_ollama(self, prompt: str, model: str = "codellama") -> str:
        """Query Ollama LLM"""
        try:
            # Prepare the request
            request_data = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            
            # Send request to Ollama
            response = requests.post("http://localhost:11434/api/generate", 
                                   json=request_data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"
    
    def query_huggingface(self, prompt: str, model: str = "microsoft/DialoGPT-medium") -> str:
        """Query Hugging Face model"""
        try:
            # This is a simplified version - in practice you'd use the Hugging Face API
            # or download the model locally
            return f"Simulated response from {model}: This is a placeholder response. In a real implementation, you would use the Hugging Face transformers library to load and run the model locally or use their API."
        except Exception as e:
            return f"Error with Hugging Face: {str(e)}"
    
    def query_local_transformers(self, prompt: str, model: str = "gpt2") -> str:
        """Query local transformers model"""
        try:
            # This would use the transformers library to load and run models locally
            return f"Simulated response from local {model}: This is a placeholder response. In a real implementation, you would load the model using transformers library and generate responses locally."
        except Exception as e:
            return f"Error with local transformers: {str(e)}"
    
    def generate_suggestions_with_llm(self, context: Dict, provider: str, model: str) -> List[Dict]:
        """Generate suggestions using the selected LLM"""
        try:
            # Build prompt
            prompt = self._build_llm_prompt(context)
            
            # Query the appropriate LLM
            if provider == "ollama":
                response = self.query_ollama(prompt, model)
            elif provider == "huggingface":
                response = self.query_huggingface(prompt, model)
            elif provider == "local_transformers":
                response = self.query_local_transformers(prompt, model)
            else:
                response = "Unknown provider"
            
            # Parse response into suggestions
            suggestions = self._parse_llm_response(response, context)
            return suggestions
            
        except Exception as e:
            return [{
                "type": "error",
                "title": "LLM Error",
                "description": f"Error generating suggestions: {str(e)}",
                "code": "",
                "priority": "high"
            }]
    
    def _build_llm_prompt(self, context: Dict) -> str:
        """Build prompt for LLM"""
        prompt = f"""You are a helpful coding assistant. Analyze the following code and provide suggestions for improvements, fixes, and best practices.

Language: {context.get('language', 'Unknown')}
File Type: {context.get('file_type', 'Unknown')}
Error Indicators: {', '.join(context.get('error_indicators', []))}

Code to analyze:
"""
        
        for i, snippet in enumerate(context.get('code_snippets', []), 1):
            prompt += f"\n--- Code Snippet {i} ---\n{snippet}\n"
        
        prompt += """

Please provide suggestions in the following format:
1. [Type] [Title]: [Description]
   Suggested fix: [Code if applicable]

Focus on:
- Syntax errors and fixes
- Best practices
- Code optimization
- Security considerations
- Readability improvements

Provide 3-5 specific, actionable suggestions."""
        
        return prompt
    
    def _parse_llm_response(self, response: str, context: Dict) -> List[Dict]:
        """Parse LLM response into structured suggestions"""
        suggestions = []
        
        # Simple parsing - in practice you'd use more sophisticated parsing
        lines = response.split('\n')
        current_suggestion = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for numbered suggestions
            if line[0].isdigit() and '.' in line:
                if current_suggestion:
                    suggestions.append(current_suggestion)
                
                # Parse suggestion header
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    header = parts[0].split(']', 1)
                    if len(header) >= 2:
                        suggestion_type = header[0].replace('[', '').replace(']', '')
                        title = header[1].strip()
                        description = parts[1].strip()
                        
                        current_suggestion = {
                            "type": suggestion_type.lower(),
                            "title": title,
                            "description": description,
                            "code": "",
                            "priority": "medium"
                        }
            
            # Look for suggested fix
            elif line.lower().startswith("suggested fix:"):
                if current_suggestion:
                    current_suggestion["code"] = line.replace("Suggested fix:", "").strip()
            
            # Look for code blocks
            elif line.startswith("```") or line.startswith("`"):
                if current_suggestion:
                    # Extract code from markdown
                    code = line.replace("```", "").replace("`", "")
                    current_suggestion["code"] = code
        
        # Add the last suggestion
        if current_suggestion:
            suggestions.append(current_suggestion)
        
        # If no structured suggestions found, create a general one
        if not suggestions:
            suggestions.append({
                "type": "general",
                "title": "LLM Analysis",
                "description": response[:200] + "..." if len(response) > 200 else response,
                "code": "",
                "priority": "medium"
            })
        
        return suggestions
    
    def setup_ui(self):
        """Setup the demo UI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🚀 Open Source LLM Copilot",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="🆓 Free AI assistance using open source models",
            font=('Arial', 12),
            foreground='#4CAF50'
        )
        subtitle_label.pack(pady=(0, 20))
        
        # LLM Selection Frame
        llm_frame = ttk.LabelFrame(main_frame, text="Select Open Source LLM", padding="10")
        llm_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Provider selection
        provider_frame = ttk.Frame(llm_frame)
        provider_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(provider_frame, text="Provider:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.provider_var = tk.StringVar(value="ollama")
        provider_combo = ttk.Combobox(
            provider_frame,
            textvariable=self.provider_var,
            values=list(self.llm_providers.keys()),
            state="readonly",
            width=20
        )
        provider_combo.pack(side=tk.LEFT, padx=(0, 20))
        provider_combo.bind('<<ComboboxSelected>>', self.on_provider_change)
        
        # Model selection
        model_frame = ttk.Frame(llm_frame)
        model_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(model_frame, text="Model:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.model_var = tk.StringVar(value="codellama")
        self.model_combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=self.llm_providers["ollama"]["models"],
            state="readonly",
            width=20
        )
        self.model_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Checking LLM availability...")
        status_label = ttk.Label(
            llm_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            foreground='#666666'
        )
        status_label.pack(pady=(10, 0))
        
        # Control frame
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Context selector
        ttk.Label(control_frame, text="Select Demo Context:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.context_var = tk.StringVar(value="Python with Syntax Errors")
        context_combo = ttk.Combobox(
            control_frame,
            textvariable=self.context_var,
            values=[
                "Python with Syntax Errors",
                "JavaScript with Reference Errors", 
                "HTML with Validation Issues"
            ],
            state="readonly",
            width=30
        )
        context_combo.pack(side=tk.LEFT, padx=(0, 20))
        context_combo.bind('<<ComboboxSelected>>', self.on_context_change)
        
        # Generate button
        generate_btn = ttk.Button(
            control_frame,
            text="Generate with LLM",
            command=self.generate_llm_suggestions
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Show overlay button
        overlay_btn = ttk.Button(
            control_frame,
            text="Show Overlay",
            command=self.show_overlay
        )
        overlay_btn.pack(side=tk.LEFT)
        
        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Context
        left_frame = ttk.LabelFrame(content_frame, text="Code to Analyze", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.context_text = scrolledtext.ScrolledText(
            left_frame,
            height=15,
            width=40,
            font=('Courier', 9)
        )
        self.context_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Suggestions
        right_frame = ttk.LabelFrame(content_frame, text="Open Source LLM Suggestions", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.suggestions_text = scrolledtext.ScrolledText(
            right_frame,
            height=15,
            width=40,
            font=('Arial', 9)
        )
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)
        
        # Load initial context
        self.update_context_display()
        self.update_llm_status()
        
    def on_provider_change(self, event):
        """Handle provider change"""
        provider = self.provider_var.get()
        self.current_provider = provider
        
        # Update available models
        if provider in self.llm_providers:
            models = self.llm_providers[provider]["models"]
            self.model_combo['values'] = models
            if models:
                self.model_var.set(models[0])
                self.current_model = models[0]
        
        self.update_llm_status()
        
    def update_llm_status(self):
        """Update LLM status display"""
        provider = self.current_provider
        
        if provider in self.llm_status:
            status = self.llm_status[provider]
            if status["available"]:
                self.status_var.set(f"✅ {self.llm_providers[provider]['name']} available")
                self.is_connected = True
            else:
                self.status_var.set(f"❌ {self.llm_providers[provider]['name']} not available")
                self.is_connected = False
        else:
            self.status_var.set("❓ Unknown provider")
            self.is_connected = False
        
    def on_context_change(self, event):
        """Handle context change"""
        selection = self.context_var.get()
        if "Python" in selection:
            self.current_context_index = 0
        elif "JavaScript" in selection:
            self.current_context_index = 1
        elif "HTML" in selection:
            self.current_context_index = 2
        
        self.update_context_display()
        
    def update_context_display(self):
        """Update the context display"""
        context = self.demo_contexts[self.current_context_index]
        
        display_text = f"""Language: {context['language']}
File Type: {context['file_type']}
Error Indicators: {', '.join(context['error_indicators'])}

Code Snippets to Analyze:
"""
        
        for i, snippet in enumerate(context['code_snippets'], 1):
            display_text += f"\n--- Snippet {i} ---\n{snippet}\n"
        
        self.context_text.delete(1.0, tk.END)
        self.context_text.insert(1.0, display_text)
        
    def generate_llm_suggestions(self):
        """Generate suggestions using the selected LLM"""
        if not self.is_connected:
            self.status_var.set("❌ LLM not available. Please check setup.")
            return
        
        context = self.demo_contexts[self.current_context_index]
        
        self.status_var.set(f"🤖 Generating suggestions with {self.current_model}...")
        self.root.update()
        
        # Generate suggestions in a separate thread
        def generate():
            suggestions = self.generate_suggestions_with_llm(
                context, self.current_provider, self.current_model
            )
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_suggestions_display(suggestions))
        
        threading.Thread(target=generate, daemon=True).start()
        
    def update_suggestions_display(self, suggestions: List[Dict]):
        """Update the suggestions display"""
        self.demo_suggestions = suggestions
        
        display_text = ""
        
        if not suggestions:
            display_text = "No suggestions generated."
        else:
            for i, suggestion in enumerate(suggestions, 1):
                display_text += f"🤖 Suggestion {i}: {suggestion['title']}\n"
                display_text += f"Type: {suggestion['type']}\n"
                display_text += f"Priority: {suggestion['priority']}\n"
                display_text += f"Description: {suggestion['description']}\n"
                if suggestion['code']:
                    display_text += f"Suggested Fix:\n{suggestion['code']}\n"
                display_text += "-" * 40 + "\n\n"
        
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, display_text)
        
        self.status_var.set(f"✅ Generated {len(suggestions)} suggestions with {self.current_model}")
        
    def show_overlay(self):
        """Show the overlay demo"""
        if not self.demo_suggestions:
            self.status_var.set("❌ No suggestions to display. Generate suggestions first.")
            return
            
        overlay_window = tk.Toplevel(self.root)
        overlay_window.title("🤖 Open Source LLM Copilot Overlay")
        overlay_window.geometry("400x500")
        overlay_window.attributes('-topmost', True)
        
        # Configure overlay appearance
        overlay_window.configure(bg='#2D3748')
        
        # Main frame
        main_frame = ttk.Frame(overlay_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🤖 Open Source LLM Copilot",
            font=('Arial', 12, 'bold'),
            foreground='#4CAF50'
        )
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text=f"🆓 Powered by {self.current_model}",
            font=('Arial', 8),
            foreground='#4CAF50'
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=(0, 10))
        
        # Suggestions
        for suggestion in self.demo_suggestions:
            suggestion_frame = ttk.Frame(main_frame)
            suggestion_frame.pack(fill=tk.X, pady=(0, 10))
            
            # Header
            header_frame = ttk.Frame(suggestion_frame)
            header_frame.pack(fill=tk.X)
            
            type_icon = "🔧" if suggestion['type'] == 'code_fix' else "✅"
            ttk.Label(header_frame, text=type_icon, font=('Arial', 12)).pack(side=tk.LEFT, padx=(0, 5))
            
            ttk.Label(
                header_frame,
                text=suggestion['title'],
                font=('Arial', 10, 'bold'),
                foreground='#4ECDC4'
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            ttk.Label(
                header_frame,
                text=suggestion['priority'].upper(),
                font=('Arial', 7),
                foreground='#888888'
            ).pack(side=tk.RIGHT)
            
            # Description
            desc_text = scrolledtext.ScrolledText(
                suggestion_frame,
                height=3,
                wrap=tk.WORD,
                font=('Arial', 9),
                bg='#2D3748',
                fg='#FFFFFF',
                relief=tk.FLAT,
                borderwidth=0
            )
            desc_text.insert(tk.END, suggestion['description'])
            desc_text.configure(state=tk.DISABLED)
            desc_text.pack(fill=tk.X, pady=(2, 5))
            
            # Code (if available)
            if suggestion['code']:
                code_frame = ttk.Frame(suggestion_frame)
                code_frame.pack(fill=tk.X, pady=(0, 5))
                
                ttk.Label(
                    code_frame,
                    text="💻 Suggested Fix:",
                    font=('Arial', 8, 'bold'),
                    foreground='#4CAF50'
                ).pack(anchor=tk.W)
                
                code_text = scrolledtext.ScrolledText(
                    code_frame,
                    height=4,
                    wrap=tk.NONE,
                    font=('Courier', 8),
                    bg='#1A202C',
                    fg='#E2E8F0',
                    relief=tk.FLAT,
                    borderwidth=1
                )
                code_text.insert(tk.END, suggestion['code'])
                code_text.configure(state=tk.DISABLED)
                code_text.pack(fill=tk.X)
        
        # Status
        ttk.Label(
            main_frame,
            text=f"Found {len(self.demo_suggestions)} suggestions - FREE!",
            font=('Arial', 8),
            foreground='#4CAF50'
        ).pack(side=tk.LEFT, pady=(10, 0))
        
        ttk.Label(
            main_frame,
            text="Press ESC to close",
            font=('Arial', 8),
            foreground='#888888'
        ).pack(side=tk.RIGHT, pady=(10, 0))
        
        # Bind escape key
        overlay_window.bind('<Escape>', lambda e: overlay_window.destroy())
        
        self.status_var.set("Open source LLM overlay displayed!")
        
    def run(self):
        """Run the demo"""
        self.root.mainloop()

def main():
    """Main demo function"""
    print("🚀 Starting Open Source LLM Copilot")
    print("🆓 Free AI assistance using open source models")
    print("=" * 60)
    
    demo = OpenSourceCopilot()
    demo.run()

if __name__ == "__main__":
    main() 