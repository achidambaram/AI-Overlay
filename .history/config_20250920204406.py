"""
Configuration settings for the Real-Time Overlay Copilot
"""

import os
from typing import Dict, Any

class Config:
    # Audio Settings
    AUDIO_SAMPLE_RATE = 16000
    AUDIO_CHUNK_SIZE = 1024
    AUDIO_CHANNELS = 1
    HOTWORD_SENSITIVITY = 0.8
    HOTWORD_PHRASE = "hey copilot"
    
    # Screen Monitoring
    SCREEN_CAPTURE_INTERVAL = 2.0  # seconds
    SCREEN_REGION = None  # None for full screen, or (x, y, width, height)
    OCR_ENABLED = True
    TEXT_DETECTION_CONFIDENCE = 0.7
    
    # AI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = "gpt-4"
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    
    # UI Settings
    OVERLAY_OPACITY = 0.95
    OVERLAY_WIDTH = 450
    OVERLAY_HEIGHT = 350
    OVERLAY_POSITION = "top-right"  # top-right, top-left, bottom-right, bottom-left
    OVERLAY_COLOR = "#1A1A1A"
    OVERLAY_TEXT_COLOR = "#E2E8F0"
    OVERLAY_BORDER_COLOR = "#3B82F6"
    OVERLAY_ACCENT_COLOR = "#10B981"
    OVERLAY_BACKGROUND_GRADIENT = True
    OVERLAY_BORDER_RADIUS = 12
    OVERLAY_SHADOW = True
    OVERLAY_BLUR = True
    
    # Enhanced UI Colors
    OVERLAY_HIGHLIGHT_COLOR = "#F59E0B"
    OVERLAY_SUCCESS_COLOR = "#10B981"
    OVERLAY_WARNING_COLOR = "#F59E0B"
    OVERLAY_ERROR_COLOR = "#EF4444"
    OVERLAY_INFO_COLOR = "#3B82F6"
    
    # Typography
    OVERLAY_FONT_FAMILY = "SF Pro Display, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    OVERLAY_FONT_SIZE_TITLE = 14
    OVERLAY_FONT_SIZE_BODY = 11
    OVERLAY_FONT_SIZE_SMALL = 9
    OVERLAY_FONT_WEIGHT_TITLE = "bold"
    OVERLAY_FONT_WEIGHT_BODY = "normal"
    
    # Animation Settings
    OVERLAY_FADE_DURATION = 0.3
    OVERLAY_SLIDE_DURATION = 0.2
    OVERLAY_HOVER_SCALE = 1.02
    OVERLAY_CLICK_SCALE = 0.98
    
    # Keyboard Shortcuts
    ACTIVATE_SHORTCUT = "ctrl+shift+c"
    DEACTIVATE_SHORTCUT = "escape"
    TOGGLE_OVERLAY_SHORTCUT = "ctrl+shift+o"
    
    # Voice Commands
    VOICE_COMMANDS = {
        "explain": "Explain the current code",
        "fix": "Suggest fixes for errors",
        "optimize": "Optimize the current code",
        "document": "Generate documentation",
        "test": "Generate test cases",
        "refactor": "Suggest refactoring",
        "debug": "Help debug issues"
    }
    
    # File Types to Monitor
    MONITORED_EXTENSIONS = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".cs",
        ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala", ".html",
        ".css", ".scss", ".sass", ".json", ".xml", ".yaml", ".yml"
    ]
    
    # Context Settings
    MAX_CONTEXT_LENGTH = 2000
    CONTEXT_WINDOW = 10  # lines before and after cursor
    IGNORE_PATTERNS = [
        "node_modules", ".git", "__pycache__", ".DS_Store",
        "*.log", "*.tmp", "*.cache"
    ]
    
    # Performance Settings
    MAX_MEMORY_USAGE = 512  # MB
    THREAD_POOL_SIZE = 4
    ENABLE_CACHING = True
    CACHE_TTL = 300  # seconds
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "copilot.log"
    ENABLE_DEBUG_MODE = False
    
    @classmethod
    def get_overlay_position(cls) -> Dict[str, int]:
        """Get overlay position coordinates based on config"""
        screen_width = 1920  # Default, will be updated at runtime
        screen_height = 1080
        
        if cls.OVERLAY_POSITION == "top-right":
            return {"x": screen_width - cls.OVERLAY_WIDTH - 20, "y": 20}
        elif cls.OVERLAY_POSITION == "top-left":
            return {"x": 20, "y": 20}
        elif cls.OVERLAY_POSITION == "bottom-right":
            return {"x": screen_width - cls.OVERLAY_WIDTH - 20, "y": screen_height - cls.OVERLAY_HEIGHT - 20}
        elif cls.OVERLAY_POSITION == "bottom-left":
            return {"x": 20, "y": screen_height - cls.OVERLAY_HEIGHT - 20}
        else:
            return {"x": 20, "y": 20}  # Default to top-left
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings"""
        if not cls.OPENAI_API_KEY:
            print("Warning: OPENAI_API_KEY not set")
            return False
        return True 