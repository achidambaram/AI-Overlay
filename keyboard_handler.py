"""
Keyboard handler module for managing shortcuts and input
"""

import keyboard
import threading
import time
from typing import Dict, List, Optional, Callable
import logging
from config import Config

class KeyboardHandler:
    def __init__(self):
        self.is_active = False
        self.registered_hotkeys = {}
        self.callbacks = {}
        self.logger = logging.getLogger(__name__)
        
        # Keyboard monitoring thread
        self.monitor_thread = None
        
        # Key state tracking
        self.pressed_keys = set()
        self.key_combinations = {}
        
    def start_monitoring(self):
        """Start keyboard monitoring"""
        if self.is_active:
            return
            
        self.is_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Keyboard monitoring started")
        
        # Register default hotkeys
        self._register_default_hotkeys()
    
    def stop_monitoring(self):
        """Stop keyboard monitoring"""
        self.is_active = False
        
        # Unregister all hotkeys
        for hotkey in self.registered_hotkeys:
            try:
                keyboard.remove_hotkey(hotkey)
            except Exception as e:
                self.logger.warning(f"Error removing hotkey {hotkey}: {e}")
        
        self.registered_hotkeys.clear()
        self.callbacks.clear()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        
        self.logger.info("Keyboard monitoring stopped")
    
    def _monitor_loop(self):
        """Main keyboard monitoring loop"""
        while self.is_active:
            try:
                # Check for key combinations
                self._check_key_combinations()
                time.sleep(0.01)  # 10ms polling interval
            except Exception as e:
                self.logger.error(f"Error in keyboard monitor loop: {e}")
                time.sleep(0.1)
    
    def _register_default_hotkeys(self):
        """Register default hotkeys from config"""
        default_hotkeys = {
            Config.ACTIVATE_SHORTCUT: "activate_copilot",
            Config.DEACTIVATE_SHORTCUT: "deactivate_copilot",
            Config.TOGGLE_OVERLAY_SHORTCUT: "toggle_overlay"
        }
        
        for hotkey, action in default_hotkeys.items():
            self.register_hotkey(hotkey, action)
    
    def register_hotkey(self, hotkey: str, action: str, callback: Optional[Callable] = None):
        """Register a hotkey with optional callback"""
        try:
            # Register with keyboard library
            keyboard.add_hotkey(hotkey, self._hotkey_callback, args=(action,))
            
            self.registered_hotkeys[hotkey] = action
            if callback:
                self.callbacks[action] = callback
            
            self.logger.info(f"Registered hotkey: {hotkey} -> {action}")
            
        except Exception as e:
            self.logger.error(f"Error registering hotkey {hotkey}: {e}")
    
    def unregister_hotkey(self, hotkey: str):
        """Unregister a hotkey"""
        try:
            if hotkey in self.registered_hotkeys:
                keyboard.remove_hotkey(hotkey)
                action = self.registered_hotkeys.pop(hotkey)
                if action in self.callbacks:
                    del self.callbacks[action]
                
                self.logger.info(f"Unregistered hotkey: {hotkey}")
                
        except Exception as e:
            self.logger.error(f"Error unregistering hotkey {hotkey}: {e}")
    
    def _hotkey_callback(self, action: str):
        """Handle hotkey callback"""
        try:
            self.logger.info(f"Hotkey triggered: {action}")
            
            # Call registered callback if available
            if action in self.callbacks:
                callback = self.callbacks[action]
                if callable(callback):
                    callback()
            
        except Exception as e:
            self.logger.error(f"Error in hotkey callback for {action}: {e}")
    
    def register_key_combination(self, keys: List[str], action: str, callback: Optional[Callable] = None):
        """Register a key combination (e.g., ['ctrl', 'shift', 'c'])"""
        try:
            key_combo = '+'.join(sorted(keys))
            self.key_combinations[key_combo] = {
                'keys': set(keys),
                'action': action,
                'callback': callback,
                'pressed': set()
            }
            
            self.logger.info(f"Registered key combination: {key_combo} -> {action}")
            
        except Exception as e:
            self.logger.error(f"Error registering key combination {keys}: {e}")
    
    def _check_key_combinations(self):
        """Check for key combinations"""
        try:
            # Get currently pressed keys
            current_pressed = set()
            
            for key_combo, combo_data in self.key_combinations.items():
                combo_keys = combo_data['keys']
                pressed_keys = combo_data['pressed']
                
                # Check which keys in the combination are currently pressed
                for key in combo_keys:
                    if keyboard.is_pressed(key):
                        current_pressed.add(key)
                    else:
                        current_pressed.discard(key)
                
                # Check if combination is complete
                if current_pressed == combo_keys and not pressed_keys:
                    # Combination just completed
                    combo_data['pressed'] = current_pressed.copy()
                    self._execute_key_combination(combo_data)
                elif current_pressed != combo_keys and pressed_keys:
                    # Combination released
                    combo_data['pressed'].clear()
                    
        except Exception as e:
            self.logger.error(f"Error checking key combinations: {e}")
    
    def _execute_key_combination(self, combo_data: Dict):
        """Execute a key combination"""
        try:
            action = combo_data['action']
            callback = combo_data['callback']
            
            self.logger.info(f"Key combination executed: {action}")
            
            if callback and callable(callback):
                callback()
                
        except Exception as e:
            self.logger.error(f"Error executing key combination: {e}")
    
    def is_key_pressed(self, key: str) -> bool:
        """Check if a specific key is currently pressed"""
        try:
            return keyboard.is_pressed(key)
        except Exception as e:
            self.logger.error(f"Error checking key {key}: {e}")
            return False
    
    def get_pressed_keys(self) -> List[str]:
        """Get list of currently pressed keys"""
        try:
            pressed = []
            for key in keyboard._listener.pressed_keys:
                pressed.append(key)
            return pressed
        except Exception as e:
            self.logger.error(f"Error getting pressed keys: {e}")
            return []
    
    def simulate_key_press(self, key: str):
        """Simulate a key press"""
        try:
            keyboard.press_and_release(key)
            self.logger.info(f"Simulated key press: {key}")
        except Exception as e:
            self.logger.error(f"Error simulating key press {key}: {e}")
    
    def simulate_key_combination(self, keys: List[str]):
        """Simulate a key combination"""
        try:
            keyboard.press_and_release('+'.join(keys))
            self.logger.info(f"Simulated key combination: {'+'.join(keys)}")
        except Exception as e:
            self.logger.error(f"Error simulating key combination {keys}: {e}")
    
    def block_key(self, key: str):
        """Block a key from being processed by other applications"""
        try:
            keyboard.block_key(key)
            self.logger.info(f"Blocked key: {key}")
        except Exception as e:
            self.logger.error(f"Error blocking key {key}: {e}")
    
    def unblock_key(self, key: str):
        """Unblock a previously blocked key"""
        try:
            keyboard.unblock_key(key)
            self.logger.info(f"Unblocked key: {key}")
        except Exception as e:
            self.logger.error(f"Error unblocking key {key}: {e}")
    
    def set_callback(self, action: str, callback: Callable):
        """Set callback for an action"""
        self.callbacks[action] = callback
        self.logger.info(f"Set callback for action: {action}")
    
    def remove_callback(self, action: str):
        """Remove callback for an action"""
        if action in self.callbacks:
            del self.callbacks[action]
            self.logger.info(f"Removed callback for action: {action}")
    
    def get_registered_hotkeys(self) -> Dict[str, str]:
        """Get all registered hotkeys"""
        return self.registered_hotkeys.copy()
    
    def get_registered_combinations(self) -> Dict[str, Dict]:
        """Get all registered key combinations"""
        return {k: {'action': v['action'], 'keys': list(v['keys'])} 
                for k, v in self.key_combinations.items()}
    
    def clear_all_hotkeys(self):
        """Clear all registered hotkeys and combinations"""
        # Clear hotkeys
        for hotkey in list(self.registered_hotkeys.keys()):
            self.unregister_hotkey(hotkey)
        
        # Clear combinations
        self.key_combinations.clear()
        
        self.logger.info("Cleared all hotkeys and combinations")
    
    def pause_monitoring(self):
        """Pause keyboard monitoring"""
        self.is_active = False
        self.logger.info("Keyboard monitoring paused")
    
    def resume_monitoring(self):
        """Resume keyboard monitoring"""
        if not self.is_active:
            self.start_monitoring()
            self.logger.info("Keyboard monitoring resumed")
    
    def cleanup(self):
        """Clean up keyboard handler"""
        self.stop_monitoring()
        self.logger.info("Keyboard handler cleaned up") 