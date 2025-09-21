#!/usr/bin/env python3
"""
Setup script for Open Source LLMs
Helps install and configure free, open source language models
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print the setup banner"""
    print("🚀" + "="*60 + "🚀")
    print("🆓 Open Source LLM Setup for Real-Time Overlay Copilot")
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

def install_ollama():
    """Install Ollama for local LLM inference"""
    print("🐐 Installing Ollama...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        try:
            # Install using Homebrew
            subprocess.run(["brew", "install", "ollama"], check=True)
            print("✅ Ollama installed via Homebrew")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama via Homebrew")
            print("Try manual installation: https://ollama.ai/download")
            return False
    
    elif system == "linux":
        try:
            # Install using curl
            install_script = "curl -fsSL https://ollama.ai/install.sh | sh"
            subprocess.run(install_script, shell=True, check=True)
            print("✅ Ollama installed via install script")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama via install script")
            print("Try manual installation: https://ollama.ai/download")
            return False
    
    elif system == "windows":
        print("🪟 Windows detected")
        print("Please download Ollama from: https://ollama.ai/download")
        print("After installation, restart this script")
        return False
    
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def install_ollama_models():
    """Install useful Ollama models"""
    print("📦 Installing Ollama models...")
    
    models = [
        "codellama",  # Best for code
        "llama2",     # General purpose
        "mistral",    # Good balance
        "gemma"       # Lightweight
    ]
    
    for model in models:
        try:
            print(f"📥 Installing {model}...")
            subprocess.run(["ollama", "pull", model], check=True, timeout=300)
            print(f"✅ {model} installed successfully")
        except subprocess.TimeoutExpired:
            print(f"⚠️  {model} installation timed out (this is normal for large models)")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {model}: {e}")
        except FileNotFoundError:
            print(f"❌ Ollama not found. Please install Ollama first.")
            return False
    
    return True

def install_huggingface_dependencies():
    """Install Hugging Face dependencies"""
    print("🤗 Installing Hugging Face dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "transformers", "torch", "accelerate", "sentencepiece"
        ], check=True)
        print("✅ Hugging Face dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Hugging Face dependencies: {e}")
        return False

def install_local_models():
    """Download and setup local models"""
    print("📥 Setting up local models...")
    
    try:
        # Create models directory
        models_dir = Path("models")
        models_dir.mkdir(exist_ok=True)
        
        # This would download models in a real implementation
        print("✅ Models directory created")
        print("📝 Note: In a real implementation, this would download models")
        return True
    except Exception as e:
        print(f"❌ Failed to setup local models: {e}")
        return False

def test_ollama():
    """Test Ollama installation"""
    print("🧪 Testing Ollama...")
    
    try:
        # Test ollama version
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama version: {result.stdout.strip()}")
            
            # Test model list
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Ollama is working correctly")
                print("📋 Available models:")
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        print(f"   - {line.split()[0]}")
                return True
            else:
                print("❌ Ollama list command failed")
                return False
        else:
            print("❌ Ollama version command failed")
            return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first.")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama test timed out")
        return False

def test_huggingface():
    """Test Hugging Face setup"""
    print("🧪 Testing Hugging Face...")
    
    try:
        import transformers
        print(f"✅ Transformers version: {transformers.__version__}")
        
        # Test basic functionality
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("gpt2", use_fast=False)
        print("✅ Hugging Face is working correctly")
        return True
    except ImportError:
        print("❌ Transformers not installed")
        return False
    except Exception as e:
        print(f"❌ Hugging Face test failed: {e}")
        return False

def create_config_file():
    """Create configuration file for open source LLMs"""
    print("⚙️  Creating configuration file...")
    
    config_content = """# Open Source LLM Configuration
# This file configures which open source LLMs to use

[ollama]
# Ollama models (run locally)
enabled = true
default_model = codellama
available_models = ["codellama", "llama2", "mistral", "gemma"]

[huggingface]
# Hugging Face models (free API or local)
enabled = true
default_model = microsoft/DialoGPT-medium
available_models = ["microsoft/DialoGPT-medium", "gpt2", "distilgpt2"]

[local_transformers]
# Local transformers models
enabled = true
default_model = gpt2
available_models = ["gpt2", "distilgpt2"]

[settings]
# General settings
timeout = 30
max_tokens = 1000
temperature = 0.7
"""
    
    try:
        with open("open_source_config.ini", "w") as f:
            f.write(config_content)
        print("✅ Configuration file created: open_source_config.ini")
        return True
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print("Choose what to install:")
    print("1. 🐐 Ollama (recommended - local LLMs)")
    print("2. 🤗 Hugging Face (free models)")
    print("3. 📦 All dependencies")
    print("4. 🧪 Test existing installation")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            setup_ollama()
            break
        elif choice == "2":
            setup_huggingface()
            break
        elif choice == "3":
            setup_all()
            break
        elif choice == "4":
            test_installation()
            break
        else:
            print("Please enter 1, 2, 3, or 4")

def setup_ollama():
    """Setup Ollama"""
    print("\n" + "="*60)
    print("🐐 Setting up Ollama...")
    print("="*60)
    
    # Install Ollama
    if install_ollama():
        # Install models
        install_ollama_models()
        
        # Test installation
        if test_ollama():
            print("\n✅ Ollama setup completed successfully!")
            print("\nNext steps:")
            print("1. Run: python open_source_copilot.py")
            print("2. Select 'ollama' as provider")
            print("3. Choose a model (codellama recommended for code)")
        else:
            print("\n❌ Ollama setup failed")
    else:
        print("\n❌ Ollama installation failed")

def setup_huggingface():
    """Setup Hugging Face"""
    print("\n" + "="*60)
    print("🤗 Setting up Hugging Face...")
    print("="*60)
    
    # Install dependencies
    if install_huggingface_dependencies():
        # Setup local models
        install_local_models()
        
        # Test installation
        if test_huggingface():
            print("\n✅ Hugging Face setup completed successfully!")
            print("\nNext steps:")
            print("1. Run: python open_source_copilot.py")
            print("2. Select 'huggingface' as provider")
            print("3. Choose a model")
        else:
            print("\n❌ Hugging Face setup failed")
    else:
        print("\n❌ Hugging Face installation failed")

def setup_all():
    """Setup all open source LLM options"""
    print("\n" + "="*60)
    print("📦 Setting up all open source LLM options...")
    print("="*60)
    
    success = True
    
    # Setup Ollama
    print("\n🐐 Setting up Ollama...")
    if not install_ollama():
        success = False
    else:
        install_ollama_models()
    
    # Setup Hugging Face
    print("\n🤗 Setting up Hugging Face...")
    if not install_huggingface_dependencies():
        success = False
    else:
        install_local_models()
    
    # Create config file
    print("\n⚙️  Creating configuration...")
    create_config_file()
    
    # Test installations
    print("\n🧪 Testing installations...")
    ollama_ok = test_ollama()
    hf_ok = test_huggingface()
    
    if success and (ollama_ok or hf_ok):
        print("\n✅ All open source LLM options setup completed!")
        print("\nAvailable options:")
        if ollama_ok:
            print("🐐 Ollama: Local LLMs (recommended)")
        if hf_ok:
            print("🤗 Hugging Face: Free models")
        print("\nNext steps:")
        print("1. Run: python open_source_copilot.py")
        print("2. Choose your preferred provider")
    else:
        print("\n❌ Some installations failed")
        if not ollama_ok:
            print("   - Ollama not working")
        if not hf_ok:
            print("   - Hugging Face not working")

def test_installation():
    """Test existing installation"""
    print("\n" + "="*60)
    print("🧪 Testing existing installation...")
    print("="*60)
    
    ollama_ok = test_ollama()
    hf_ok = test_huggingface()
    
    print("\n📊 Test Results:")
    if ollama_ok:
        print("✅ Ollama: Working")
    else:
        print("❌ Ollama: Not working")
    
    if hf_ok:
        print("✅ Hugging Face: Working")
    else:
        print("❌ Hugging Face: Not working")
    
    if ollama_ok or hf_ok:
        print("\n✅ At least one open source LLM is working!")
        print("You can run: python open_source_copilot.py")
    else:
        print("\n❌ No open source LLMs are working")
        print("Please run setup again or install manually")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1) 