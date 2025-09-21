"""
Audio processing module for hotword detection and voice commands
"""

import pyaudio
import wave
import threading
import time
import numpy as np
import speech_recognition as sr
from typing import Optional, Callable, Dict, List
import logging
from config import Config

class AudioProcessor:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.hotword_detected = False
        self.audio_thread = None
        self.logger = logging.getLogger(__name__)
        
        # Audio settings
        self.sample_rate = Config.AUDIO_SAMPLE_RATE
        self.chunk_size = Config.AUDIO_CHUNK_SIZE
        self.channels = Config.AUDIO_CHANNELS
        self.format = pyaudio.paInt16
        
        # Callbacks
        self.hotword_callback = None
        self.voice_command_callback = None
        
        # Voice command patterns
        self.voice_commands = Config.VOICE_COMMANDS
        
    def start_listening(self, hotword_callback: Optional[Callable] = None, 
                       voice_command_callback: Optional[Callable] = None):
        """Start listening for hotwords and voice commands"""
        if self.is_listening:
            return
            
        self.hotword_callback = hotword_callback
        self.voice_command_callback = voice_command_callback
        self.is_listening = True
        
        self.audio_thread = threading.Thread(target=self._audio_loop, daemon=True)
        self.audio_thread.start()
        self.logger.info("Audio listening started")
    
    def stop_listening(self):
        """Stop listening for audio"""
        self.is_listening = False
        if self.audio_thread:
            self.audio_thread.join(timeout=1)
        self.logger.info("Audio listening stopped")
    
    def _audio_loop(self):
        """Main audio processing loop"""
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            self.logger.info("Audio stream opened")
            
            while self.is_listening:
                try:
                    # Read audio data
                    audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                    
                    # Check for hotword
                    if self._detect_hotword(audio_data):
                        self.hotword_detected = True
                        self.logger.info("Hotword detected!")
                        
                        if self.hotword_callback:
                            self.hotword_callback()
                        
                        # Listen for voice command after hotword
                        self._listen_for_command(stream)
                        
                except Exception as e:
                    self.logger.error(f"Error in audio loop: {e}")
                    time.sleep(0.1)
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            self.logger.error(f"Error opening audio stream: {e}")
    
    def _detect_hotword(self, audio_data: bytes) -> bool:
        """Detect hotword in audio data"""
        try:
            # Convert audio data to audio source
            audio_source = sr.AudioData(audio_data, self.sample_rate, 2)
            
            # Use speech recognition to detect hotword
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
            
            # Try to recognize speech
            try:
                text = self.recognizer.recognize_google(audio_source, language='en-US')
                text = text.lower().strip()
                
                # Check if hotword is in the recognized text
                if Config.HOTWORD_PHRASE in text:
                    return True
                    
            except sr.UnknownValueError:
                pass  # No speech detected
            except sr.RequestError as e:
                self.logger.warning(f"Speech recognition service error: {e}")
                
        except Exception as e:
            self.logger.error(f"Error detecting hotword: {e}")
        
        return False
    
    def _listen_for_command(self, stream):
        """Listen for voice command after hotword detection"""
        try:
            self.logger.info("Listening for voice command...")
            
            # Record audio for command
            frames = []
            recording_duration = 3  # seconds
            frames_needed = int(self.sample_rate / self.chunk_size * recording_duration)
            
            for _ in range(frames_needed):
                if not self.is_listening:
                    break
                audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(audio_data)
            
            if frames:
                # Combine frames
                audio_data = b''.join(frames)
                audio_source = sr.AudioData(audio_data, self.sample_rate, 2)
                
                # Recognize command
                try:
                    text = self.recognizer.recognize_google(audio_source, language='en-US')
                    text = text.lower().strip()
                    
                    self.logger.info(f"Voice command detected: {text}")
                    
                    # Process command
                    self._process_voice_command(text)
                    
                except sr.UnknownValueError:
                    self.logger.info("No voice command detected")
                except sr.RequestError as e:
                    self.logger.warning(f"Speech recognition service error: {e}")
                    
        except Exception as e:
            self.logger.error(f"Error listening for command: {e}")
    
    def _process_voice_command(self, text: str):
        """Process recognized voice command"""
        try:
            # Check for known commands
            for command, description in self.voice_commands.items():
                if command in text:
                    self.logger.info(f"Executing command: {command} - {description}")
                    
                    if self.voice_command_callback:
                        self.voice_command_callback(command, text)
                    return
            
            # If no specific command found, treat as general query
            self.logger.info(f"General query: {text}")
            if self.voice_command_callback:
                self.voice_command_callback("query", text)
                
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
    
    def record_audio(self, duration: float = 5.0) -> Optional[bytes]:
        """Record audio for a specified duration"""
        try:
            stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            frames = []
            frames_needed = int(self.sample_rate / self.chunk_size * duration)
            
            for _ in range(frames_needed):
                audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(audio_data)
            
            stream.stop_stream()
            stream.close()
            
            return b''.join(frames)
            
        except Exception as e:
            self.logger.error(f"Error recording audio: {e}")
            return None
    
    def save_audio(self, audio_data: bytes, filename: str):
        """Save audio data to WAV file"""
        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.sample_rate)
                wf.writeframes(audio_data)
            
            self.logger.info(f"Audio saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving audio: {e}")
    
    def get_audio_devices(self) -> List[Dict]:
        """Get list of available audio input devices"""
        devices = []
        
        try:
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:  # Input device
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
        except Exception as e:
            self.logger.error(f"Error getting audio devices: {e}")
        
        return devices
    
    def set_audio_device(self, device_index: int):
        """Set audio input device"""
        try:
            device_info = self.audio.get_device_info_by_index(device_index)
            if device_info['maxInputChannels'] > 0:
                self.logger.info(f"Audio device set to: {device_info['name']}")
                return True
            else:
                self.logger.error("Selected device is not an input device")
                return False
        except Exception as e:
            self.logger.error(f"Error setting audio device: {e}")
            return False
    
    def cleanup(self):
        """Clean up audio resources"""
        self.stop_listening()
        self.audio.terminate()
        self.logger.info("Audio processor cleaned up") 