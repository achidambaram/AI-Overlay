#!/usr/bin/env python3
"""
Real-Time Overlay Copilot - Main Application
A screen-aware AI coding copilot that provides real-time assistance for developers.
"""

import sys
import os
import signal
import threading
import time
import logging
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from config import Config
from screen_monitor import ScreenMonitor
from audio_processor import AudioProcessor
from ai_engine import AIEngine
from overlay_ui import OverlayUI
from keyboard_handler import KeyboardHandler

class RealTimeCopilot:
    def __init__(self):
        self.logger = self._setup_logging()
        self.logger.info("🚀 Starting Real-Time Overlay Copilot")
        
        # Initialize components
        self.screen_monitor = None
        self.audio_processor = None
        self.ai_engine = None
        self.overlay_ui = None
        self.keyboard_handler = None
        
        # State management
        self.is_running = False
        self.is_active = False
        self.current_context = {}
        self.last_suggestions = []
        
        # Threading
        self.main_thread = None
        self.suggestion_thread = None
        
        # Initialize components
        self._initialize_components()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def _initialize_components(self):
        """Initialize all copilot components"""
        try:
            # Validate configuration
            if not Config.validate():
                self.logger.warning("Configuration validation failed")
            
            # Initialize screen monitor
            self.screen_monitor = ScreenMonitor()
            self.logger.info("✅ Screen monitor initialized")
            
            # Initialize audio processor
            self.audio_processor = AudioProcessor()
            self.logger.info("✅ Audio processor initialized")
            
            # Initialize AI engine
            self.ai_engine = AIEngine()
            self.logger.info("✅ AI engine initialized")
            
            # Initialize overlay UI
            self.overlay_ui = OverlayUI()
            self.logger.info("✅ Overlay UI initialized")
            
            # Initialize keyboard handler
            self.keyboard_handler = KeyboardHandler()
            self.logger.info("✅ Keyboard handler initialized")
            
            # Set up callbacks
            self._setup_callbacks()
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing components: {e}")
            raise
    
    def _setup_callbacks(self):
        """Setup callback functions between components"""
        try:
            # Audio processor callbacks
            self.audio_processor.start_listening(
                hotword_callback=self._on_hotword_detected,
                voice_command_callback=self._on_voice_command
            )
            
            # Overlay UI callbacks
            self.overlay_ui.set_callbacks(
                on_suggestion_click=self._on_suggestion_click,
                on_close=self._on_overlay_close
            )
            
            # Keyboard handler callbacks
            self.keyboard_handler.set_callback("activate_copilot", self._activate_copilot)
            self.keyboard_handler.set_callback("deactivate_copilot", self._deactivate_copilot)
            self.keyboard_handler.set_callback("toggle_overlay", self._toggle_overlay)
            
        except Exception as e:
            self.logger.error(f"Error setting up callbacks: {e}")
    
    def start(self):
        """Start the copilot"""
        try:
            if self.is_running:
                self.logger.warning("Copilot is already running")
                return
            
            self.logger.info("🚀 Starting Real-Time Overlay Copilot...")
            
            # Start all components
            self.screen_monitor.start_monitoring()
            self.keyboard_handler.start_monitoring()
            
            # Set running state
            self.is_running = True
            self.is_active = True
            
            # Start main loop
            self.main_thread = threading.Thread(target=self._main_loop, daemon=True)
            self.main_thread.start()
            
            # Start suggestion generation thread
            self.suggestion_thread = threading.Thread(target=self._suggestion_loop, daemon=True)
            self.suggestion_thread.start()
            
            self.logger.info("✅ Copilot started successfully")
            self.logger.info("🎤 Say 'Hey Copilot' to activate")
            self.logger.info(f"⌨️  Press {Config.ACTIVATE_SHORTCUT} to activate manually")
            
            # Show initial overlay
            self._show_welcome_overlay()
            
        except Exception as e:
            self.logger.error(f"❌ Error starting copilot: {e}")
            raise
    
    def stop(self):
        """Stop the copilot"""
        try:
            if not self.is_running:
                return
            
            self.logger.info("🛑 Stopping Real-Time Overlay Copilot...")
            
            # Stop all components
            self.is_running = False
            self.is_active = False
            
            if self.screen_monitor:
                self.screen_monitor.stop_monitoring()
            
            if self.audio_processor:
                self.audio_processor.stop_listening()
            
            if self.keyboard_handler:
                self.keyboard_handler.stop_monitoring()
            
            if self.overlay_ui:
                self.overlay_ui.destroy()
            
            self.logger.info("✅ Copilot stopped successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping copilot: {e}")
    
    def _main_loop(self):
        """Main application loop"""
        try:
            while self.is_running:
                # Update context from screen monitor
                self.current_context = self.screen_monitor.get_current_context()
                
                # Check for errors or issues
                self._check_for_issues()
                
                time.sleep(1)  # 1 second interval
                
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
    
    def _suggestion_loop(self):
        """Loop for generating AI suggestions"""
        try:
            while self.is_running:
                if self.is_active and self.current_context:
                    # Generate suggestions based on current context
                    suggestions = self.ai_engine.generate_suggestions(self.current_context)
                    
                    if suggestions and not suggestions.get("error"):
                        self.last_suggestions = suggestions.get("suggestions", [])
                        
                        # Update overlay if visible
                        if self.overlay_ui.is_visible:
                            self.overlay_ui.update_suggestions(self.last_suggestions)
                
                time.sleep(5)  # Generate suggestions every 5 seconds
                
        except Exception as e:
            self.logger.error(f"Error in suggestion loop: {e}")
    
    def _check_for_issues(self):
        """Check for issues in current context"""
        try:
            if not self.current_context:
                return
            
            # Check for error indicators
            error_indicators = self.current_context.get("error_indicators", [])
            if error_indicators and self.is_active:
                self.logger.info(f"⚠️  Error indicators detected: {error_indicators}")
                
                # Generate error-specific suggestions
                error_suggestions = self.ai_engine.suggest_fixes(
                    str(error_indicators),
                    self.current_context.get("text_content", "")
                )
                
                if error_suggestions and not error_suggestions.get("error"):
                    self._show_error_suggestions(error_suggestions)
            
        except Exception as e:
            self.logger.error(f"Error checking for issues: {e}")
    
    def _on_hotword_detected(self):
        """Handle hotword detection"""
        try:
            self.logger.info("🎤 Hotword detected!")
            self._activate_copilot()
            
        except Exception as e:
            self.logger.error(f"Error handling hotword: {e}")
    
    def _on_voice_command(self, command: str, text: str):
        """Handle voice command"""
        try:
            self.logger.info(f"🎤 Voice command: {command} - {text}")
            
            # Generate suggestions based on voice command
            suggestions = self.ai_engine.generate_suggestions(
                self.current_context,
                command=command,
                query=text
            )
            
            if suggestions and not suggestions.get("error"):
                self._show_suggestions(suggestions)
            
        except Exception as e:
            self.logger.error(f"Error handling voice command: {e}")
    
    def _activate_copilot(self):
        """Activate the copilot"""
        try:
            if not self.is_active:
                self.is_active = True
                self.logger.info("✅ Copilot activated")
                
                # Show current suggestions
                if self.last_suggestions:
                    self._show_suggestions({"suggestions": self.last_suggestions})
                else:
                    self._show_welcome_overlay()
            
        except Exception as e:
            self.logger.error(f"Error activating copilot: {e}")
    
    def _deactivate_copilot(self):
        """Deactivate the copilot"""
        try:
            if self.is_active:
                self.is_active = False
                self.logger.info("⏸️  Copilot deactivated")
                
                # Hide overlay
                if self.overlay_ui:
                    self.overlay_ui.hide_overlay()
            
        except Exception as e:
            self.logger.error(f"Error deactivating copilot: {e}")
    
    def _toggle_overlay(self):
        """Toggle overlay visibility"""
        try:
            if self.overlay_ui.is_visible:
                self.overlay_ui.hide_overlay()
            else:
                self._show_suggestions({"suggestions": self.last_suggestions})
            
        except Exception as e:
            self.logger.error(f"Error toggling overlay: {e}")
    
    def _show_suggestions(self, suggestions: Dict):
        """Show suggestions in overlay"""
        try:
            if not self.is_active:
                return
            
            suggestion_list = suggestions.get("suggestions", [])
            if suggestion_list:
                self.overlay_ui.create_overlay(suggestion_list)
                self.logger.info(f"📋 Showing {len(suggestion_list)} suggestions")
            
        except Exception as e:
            self.logger.error(f"Error showing suggestions: {e}")
    
    def _show_error_suggestions(self, error_suggestions: Dict):
        """Show error-specific suggestions"""
        try:
            fixes = error_suggestions.get("fixes", [])
            if fixes:
                # Convert fixes to suggestion format
                suggestions = []
                for fix in fixes:
                    suggestions.append({
                        "type": "code_fix",
                        "title": "Error Fix",
                        "description": fix.get("description", ""),
                        "code": fix.get("code", ""),
                        "priority": "high"
                    })
                
                self._show_suggestions({"suggestions": suggestions})
            
        except Exception as e:
            self.logger.error(f"Error showing error suggestions: {e}")
    
    def _show_welcome_overlay(self):
        """Show welcome overlay"""
        try:
            welcome_suggestions = [
                {
                    "type": "general",
                    "title": "Welcome to AI Copilot! 🤖",
                    "description": "I'm here to help you with your coding. Say 'Hey Copilot' or use keyboard shortcuts to get started.",
                    "code": "",
                    "priority": "low"
                },
                {
                    "type": "best_practice",
                    "title": "Available Commands",
                    "description": "Try saying: explain, fix, optimize, document, test, refactor, or debug",
                    "code": "",
                    "priority": "low"
                }
            ]
            
            self.overlay_ui.create_overlay(welcome_suggestions)
            
        except Exception as e:
            self.logger.error(f"Error showing welcome overlay: {e}")
    
    def _on_suggestion_click(self, suggestion: Dict):
        """Handle suggestion click"""
        try:
            self.logger.info(f"📋 Suggestion clicked: {suggestion.get('title', 'Unknown')}")
            
            # Here you could implement suggestion application logic
            # For now, just log the action
            
        except Exception as e:
            self.logger.error(f"Error handling suggestion click: {e}")
    
    def _on_overlay_close(self):
        """Handle overlay close"""
        try:
            self.logger.info("📋 Overlay closed")
            # Could implement additional logic here
            
        except Exception as e:
            self.logger.error(f"Error handling overlay close: {e}")
    
    def get_status(self) -> Dict:
        """Get current copilot status"""
        return {
            "is_running": self.is_running,
            "is_active": self.is_active,
            "context": self.current_context,
            "suggestions_count": len(self.last_suggestions),
            "components": {
                "screen_monitor": self.screen_monitor.is_monitoring if self.screen_monitor else False,
                "audio_processor": self.audio_processor.is_listening if self.audio_processor else False,
                "ai_engine": self.ai_engine.is_initialized if self.ai_engine else False,
                "overlay_ui": self.overlay_ui.is_visible if self.overlay_ui else False,
                "keyboard_handler": self.keyboard_handler.is_active if self.keyboard_handler else False
            }
        }

def signal_handler(signum, frame):
    """Handle system signals for graceful shutdown"""
    print("\n🛑 Received shutdown signal. Stopping copilot...")
    if copilot:
        copilot.stop()
    sys.exit(0)

def main():
    """Main entry point"""
    global copilot
    
    try:
        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Create and start copilot
        copilot = RealTimeCopilot()
        copilot.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received. Stopping copilot...")
            copilot.stop()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if copilot:
            copilot.stop()
        sys.exit(1)

if __name__ == "__main__":
    copilot = None
    main() 