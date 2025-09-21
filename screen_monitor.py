"""
Screen monitoring and analysis module for the Real-Time Overlay Copilot
"""

import cv2
import numpy as np
import pytesseract
import mss
import threading
import time
from typing import Optional, Dict, List, Tuple
from PIL import Image
import logging
from config import Config

class ScreenMonitor:
    def __init__(self):
        self.sct = mss.mss()
        self.is_monitoring = False
        self.current_context = {}
        self.last_capture_time = 0
        self.screen_width = 1920
        self.screen_height = 1080
        self.logger = logging.getLogger(__name__)
        
        # Initialize screen dimensions
        self._update_screen_dimensions()
        
    def _update_screen_dimensions(self):
        """Update screen dimensions from system"""
        try:
            monitor = self.sct.monitors[1]  # Primary monitor
            self.screen_width = monitor["width"]
            self.screen_height = monitor["height"]
            self.logger.info(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
        except Exception as e:
            self.logger.warning(f"Could not get screen dimensions: {e}")
    
    def start_monitoring(self):
        """Start screen monitoring in a separate thread"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Screen monitoring started")
    
    def stop_monitoring(self):
        """Stop screen monitoring"""
        self.is_monitoring = False
        self.logger.info("Screen monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                current_time = time.time()
                if current_time - self.last_capture_time >= Config.SCREEN_CAPTURE_INTERVAL:
                    self._capture_and_analyze()
                    self.last_capture_time = current_time
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
            except Exception as e:
                self.logger.error(f"Error in monitor loop: {e}")
                time.sleep(1)
    
    def _capture_and_analyze(self):
        """Capture screen and analyze content"""
        try:
            # Capture screen
            screenshot = self._capture_screen()
            if screenshot is None:
                return
            
            # Analyze content
            analysis = self._analyze_screen_content(screenshot)
            
            # Update context
            self.current_context.update(analysis)
            
        except Exception as e:
            self.logger.error(f"Error capturing and analyzing screen: {e}")
    
    def _capture_screen(self) -> Optional[np.ndarray]:
        """Capture screen or region"""
        try:
            if Config.SCREEN_REGION:
                x, y, width, height = Config.SCREEN_REGION
                monitor = {"top": y, "left": x, "width": width, "height": height}
            else:
                monitor = self.sct.monitors[1]  # Primary monitor
            
            screenshot = self.sct.grab(monitor)
            return np.array(screenshot)
            
        except Exception as e:
            self.logger.error(f"Error capturing screen: {e}")
            return None
    
    def _analyze_screen_content(self, screenshot: np.ndarray) -> Dict:
        """Analyze screen content for text, code, and context"""
        analysis = {
            "timestamp": time.time(),
            "text_content": "",
            "code_detected": False,
            "file_type": None,
            "error_indicators": [],
            "suggestions_context": ""
        }
        
        try:
            # Convert to PIL Image for OCR
            pil_image = Image.fromarray(screenshot)
            
            # Extract text using OCR
            if Config.OCR_ENABLED:
                text = pytesseract.image_to_string(pil_image)
                analysis["text_content"] = text
                
                # Analyze for code patterns
                code_analysis = self._detect_code_patterns(text)
                analysis.update(code_analysis)
                
                # Look for error indicators
                error_indicators = self._detect_error_indicators(text)
                analysis["error_indicators"] = error_indicators
                
                # Generate context for AI suggestions
                analysis["suggestions_context"] = self._generate_suggestions_context(text, code_analysis)
            
        except Exception as e:
            self.logger.error(f"Error analyzing screen content: {e}")
        
        return analysis
    
    def _detect_code_patterns(self, text: str) -> Dict:
        """Detect code patterns and file types"""
        analysis = {
            "code_detected": False,
            "file_type": None,
            "language": None,
            "code_snippets": []
        }
        
        # Common code patterns
        code_patterns = {
            "python": [r"def\s+\w+", r"import\s+\w+", r"class\s+\w+", r"if\s+__name__"],
            "javascript": [r"function\s+\w+", r"const\s+\w+", r"let\s+\w+", r"var\s+\w+", r"console\.log"],
            "typescript": [r"interface\s+\w+", r"type\s+\w+", r"const\s+\w+:\s+\w+", r"function\s+\w+\(.*\):"],
            "java": [r"public\s+class", r"public\s+static\s+void", r"import\s+java"],
            "cpp": [r"#include", r"int\s+main", r"class\s+\w+", r"std::"],
            "html": [r"<!DOCTYPE", r"<html", r"<div", r"<script"],
            "css": [r"\.\w+\s*\{", r"#\w+\s*\{", r"@media", r"@keyframes"]
        }
        
        import re
        
        for language, patterns in code_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    analysis["code_detected"] = True
                    analysis["language"] = language
                    
                    # Determine file type
                    for ext in Config.MONITORED_EXTENSIONS:
                        if ext.startswith("." + language) or (language == "javascript" and ext in [".js", ".jsx"]) or (language == "typescript" and ext in [".ts", ".tsx"]):
                            analysis["file_type"] = ext
                            break
                    
                    # Extract code snippets
                    snippets = re.findall(r'[\w\s\(\)\{\}\[\]]{20,}', text)
                    analysis["code_snippets"] = snippets[:5]  # Limit to 5 snippets
                    break
            
            if analysis["code_detected"]:
                break
        
        return analysis
    
    def _detect_error_indicators(self, text: str) -> List[str]:
        """Detect error indicators in text"""
        error_indicators = []
        
        error_patterns = [
            r"error:", r"exception:", r"traceback:", r"failed:", r"failure:",
            r"undefined", r"null", r"nan", r"infinity", r"stack trace",
            r"syntax error", r"type error", r"reference error", r"runtime error",
            r"import error", r"module not found", r"file not found",
            r"permission denied", r"access denied", r"timeout", r"connection refused"
        ]
        
        import re
        
        for pattern in error_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                error_indicators.append(pattern.replace(":", "").replace("_", " ").title())
        
        return list(set(error_indicators))  # Remove duplicates
    
    def _generate_suggestions_context(self, text: str, code_analysis: Dict) -> str:
        """Generate context for AI suggestions"""
        context_parts = []
        
        if code_analysis["code_detected"]:
            context_parts.append(f"Language: {code_analysis['language']}")
            if code_analysis["code_snippets"]:
                context_parts.append("Code snippets detected")
        
        # Add recent text (last 500 characters)
        recent_text = text[-500:] if len(text) > 500 else text
        if recent_text.strip():
            context_parts.append(f"Recent content: {recent_text.strip()}")
        
        return " | ".join(context_parts)
    
    def get_current_context(self) -> Dict:
        """Get current screen context"""
        return self.current_context.copy()
    
    def get_screen_dimensions(self) -> Tuple[int, int]:
        """Get current screen dimensions"""
        return self.screen_width, self.screen_height
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> Optional[np.ndarray]:
        """Capture a specific region of the screen"""
        try:
            monitor = {"top": y, "left": x, "width": width, "height": height}
            screenshot = self.sct.grab(monitor)
            return np.array(screenshot)
        except Exception as e:
            self.logger.error(f"Error capturing region: {e}")
            return None 