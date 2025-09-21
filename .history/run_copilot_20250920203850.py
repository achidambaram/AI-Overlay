#!/usr/bin/env python3
"""
One-Command Launcher for Real-Time Overlay Copilot
Handles setup, configuration, and running automatically.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time

def print_banner():
    """Print the copilot banner"""
    print("🚀" + "="*60 + "🚀")
    print("🤖 Real-Time Overlay Copilot - One-Command Launcher")
    print("🚀" + "="*60 + "🚀")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'opencv-python', 'numpy', 'pyaudio', 'speechrecognition',
        'openai', 'python-dotenv', 'pytesseract', 'mss', 'keyboard'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'pyaudio':
                import pyaudio
            elif package == 'speechrecognition':
                import speech_recognition
            elif package == 'openai':
                import openai
            elif package == 'python-dotenv':
                import dotenv
            elif package == 'pytesseract':
                import pytesseract
            elif package == 'mss':
                import mss
            elif package == 'keyboard':
                import keyboard
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All Python packages found")
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_system_dependencies():
    """Check system dependencies"""
    print("🔍 Checking system dependencies...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        # Check for Homebrew
        try:
            subprocess.run(["brew", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
            return False
        
        # Check for Tesseract
        try:
            subprocess.run(["tesseract", "--version"], check=True, capture_output=True)
            print("✅ Tesseract found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Tesseract not found. Installing...")
            subprocess.run(["brew", "install", "tesseract"], check=True)
        
        # Check for PortAudio
        try:
            subprocess.run(["brew", "list", "portaudio"], check=True, capture_output=True)
            print("✅ PortAudio found")
        except subprocess.CalledProcessError:
            print("⚠️  PortAudio not found. Installing...")
            subprocess.run(["brew", "install", "portaudio"], check=True)
    
    elif system == "linux":
        # Check for Tesseract
        try:
            subprocess.run(["tesseract", "--version"], check=True, capture_output=True)
            print("✅ Tesseract found")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Tesseract not found. Please install:")
            print("   sudo apt-get install tesseract-ocr")
            return False
        
        # Check for PortAudio
        try:
            subprocess.run(["pkg-config", "--exists", "portaudio-2.0"], check=True, capture_output=True)
            print("✅ PortAudio found")
        except subprocess.CalledProcessError:
            print("⚠️  PortAudio not found. Please install:")
            print("   sudo apt-get install portaudio19-dev")
            return False
    
    elif system == "windows":
        print("🪟 Windows detected - please ensure you have:")
        print("1. Tesseract OCR installed")
        print("2. PortAudio installed")
        print("3. Visual C++ Build Tools")
    
    return True

def setup_environment():
    """Setup environment configuration"""
    print("⚙️  Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path("env_example.txt")
    
    if env_file.exists():
        print("✅ .env file already exists")
        
        # Check if API key is set
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_openai_api_key_here" in content or "OPENAI_API_KEY=" not in content:
                print("⚠️  Please add your OpenAI API key to .env file")
                print("   Get one from: https://platform.openai.com/api-keys")
                return False
            else:
                print("✅ OpenAI API key found")
                return True
    else:
        if env_example.exists():
            # Copy example to .env
            try:
                with open(env_example, 'r') as f:
                    content = f.read()
                
                with open(env_file, 'w') as f:
                    f.write(content)
                
                print("✅ Created .env file from template")
                print("⚠️  Please add your OpenAI API key to .env file")
                print("   Get one from: https://platform.openai.com/api-keys")
                return False
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
        except Exception as e:
            print(f"❌ Error creating directory {directory}: {e}")
            return False
    
    print("✅ Directories created")
    return True

def run_demo():
    """Run the demo version"""
    print("🎯 Running demo version...")
    print("This shows the copilot's capabilities without requiring full setup.")
    print()
    
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Demo failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
        return True

def run_free_copilot():
    """Run the free copilot version"""
    print("💰 Running free copilot version...")
    print("This version uses local rule-based analysis - no API costs!")
    print()
    
    try:
        subprocess.run([sys.executable, "free_copilot.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Free copilot failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Free copilot stopped by user")
        return True

def run_open_source_copilot():
    """Run the open source LLM copilot version"""
    print("🆓 Running open source LLM copilot...")
    print("This version uses free, open source AI models!")
    print()
    
    try:
        subprocess.run([sys.executable, "open_source_copilot.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Open source copilot failed: {e}")
        print("You may need to run setup first: python setup_open_source.py")
        return False
    except KeyboardInterrupt:
        print("\n👋 Open source copilot stopped by user")
        return True

def run_copilot():
    """Run the main copilot"""
    print("🚀 Starting Real-Time Overlay Copilot...")
    print()
    print("🎤 Say 'Hey Copilot' to activate")
    print("⌨️  Press Ctrl+Shift+C to activate manually")
    print("🔴 Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Copilot failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Copilot stopped by user")
        return True

def main():
    """Main launcher function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if user wants demo or full version
    print("Choose an option:")
    print("1. 🎯 Demo (no setup required)")
    print("2. 🚀 Full Copilot (requires OpenAI API key)")
    print("3. 💰 Free Copilot (no API costs - rule-based)")
    print("4. 🆓 Open Source LLM Copilot (free AI models)")
    print("5. 🔧 Setup only")
    
    while True:
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            return run_demo()
        elif choice == "2":
            break
        elif choice == "3":
            return run_free_copilot()
        elif choice == "4":
            return run_open_source_copilot()
        elif choice == "5":
            return setup_only()
        else:
            print("Please enter 1, 2, 3, 4, or 5")
    
    print("\n" + "="*60)
    print("🚀 Setting up Full Copilot...")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Check system dependencies
    if not check_system_dependencies():
        print("❌ System dependencies not met")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("\n⚠️  Environment setup incomplete")
        print("Please add your OpenAI API key to .env file and run again")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    print("\n✅ Setup complete!")
    print("🚀 Starting copilot...")
    print()
    
    # Run the copilot
    return run_copilot()

def setup_only():
    """Setup only mode"""
    print("\n" + "="*60)
    print("🔧 Setup Only Mode")
    print("="*60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return False
    
    # Check system dependencies
    if not check_system_dependencies():
        print("❌ System dependencies not met")
        return False
    
    # Setup environment
    if not setup_environment():
        print("\n⚠️  Environment setup incomplete")
        print("Please add your OpenAI API key to .env file")
        return False
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        return False
    
    print("\n✅ Setup complete!")
    print("You can now run: python main.py")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 