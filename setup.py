#!/usr/bin/env python3
"""
Setup script for Real-Time Overlay Copilot
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_system_dependencies():
    """Install system dependencies based on platform"""
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("🍎 Installing macOS dependencies...")
        commands = [
            ("brew install tesseract", "Installing Tesseract OCR"),
            ("brew install portaudio", "Installing PortAudio"),
        ]
    elif system == "linux":
        print("🐧 Installing Linux dependencies...")
        commands = [
            ("sudo apt-get update", "Updating package list"),
            ("sudo apt-get install -y tesseract-ocr", "Installing Tesseract OCR"),
            ("sudo apt-get install -y portaudio19-dev", "Installing PortAudio"),
            ("sudo apt-get install -y python3-tk", "Installing Tkinter"),
        ]
    elif system == "windows":
        print("🪟 Windows detected - please install dependencies manually:")
        print("1. Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install PortAudio from: http://www.portaudio.com/download.html")
        return True
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    print("🐍 Installing Python dependencies...")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        return False
    
    # Install dependencies
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing Python packages"):
        return False
    
    return True

def setup_environment():
    """Setup environment configuration"""
    print("⚙️  Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        # Copy example to .env
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    else:
        print("❌ env_example.txt not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["logs", "cache", "temp"]
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            print(f"✅ Created directory: {directory}")
        except Exception as e:
            print(f"❌ Error creating directory {directory}: {e}")
            return False
    
    return True

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import cv2
        import numpy
        import pyaudio
        import speech_recognition
        import openai
        import tkinter
        import keyboard
        import mss
        import pytesseract
        
        print("✅ All required packages imported successfully")
        
        # Test Tesseract
        try:
            pytesseract.get_tesseract_version()
            print("✅ Tesseract OCR working")
        except Exception as e:
            print(f"⚠️  Tesseract OCR not working: {e}")
        
        # Test audio
        try:
            audio = pyaudio.PyAudio()
            device_count = audio.get_device_count()
            print(f"✅ Audio system working ({device_count} devices found)")
            audio.terminate()
        except Exception as e:
            print(f"⚠️  Audio system not working: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Real-Time Overlay Copilot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install system dependencies
    if not install_system_dependencies():
        print("❌ Failed to install system dependencies")
        sys.exit(1)
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Run: python main.py")
    print("3. Say 'Hey Copilot' or press Ctrl+Shift+C to activate")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 