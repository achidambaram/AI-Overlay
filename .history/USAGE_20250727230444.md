# 🚀 How to Run the Real-Time Overlay Copilot

## ⚡ One-Command Options

### Option 1: Smart Launcher (Recommended)
```bash
python run_copilot.py
```
This intelligent launcher will:
- ✅ Check your Python version
- ✅ Install missing dependencies automatically
- ✅ Set up system dependencies (Tesseract, PortAudio)
- ✅ Create configuration files
- ✅ Guide you through API key setup
- ✅ Run the program

### Option 2: Shell Script (Easiest)
```bash
./copilot
```
This runs the same smart launcher but from a shell script.

### Option 3: Direct Demo (No Setup)
```bash
python demo.py
```
See the copilot in action immediately without any setup!

## 🔧 Step-by-Step Manual Setup

### 1. Install System Dependencies

**macOS:**
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install tesseract portaudio
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr portaudio19-dev python3-tk
```

**Windows:**
- Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
- Download PortAudio from: http://www.portaudio.com/download.html

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Configuration
```bash
# Copy environment template
cp env_example.txt .env

# Edit .env file and add your OpenAI API key
nano .env
```

### 4. Run the Program
```bash
python main.py
```

## 🎯 Quick Start Guide

### First Time Users

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd AI-Overlay-Copilot
   ```

2. **Run the smart launcher:**
   ```bash
   python run_copilot.py
   ```

3. **Choose option 1 (Demo) to see it work:**
   - No setup required
   - Shows all features
   - Interactive interface

4. **Choose option 2 (Full Copilot) for real use:**
   - Follow the setup prompts
   - Add your OpenAI API key when prompted
   - The launcher handles everything else

### Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key
5. Add it to your `.env` file:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

## 🎮 Using the Copilot

### Voice Commands
- **"Hey Copilot"** - Activate the copilot
- **"explain"** - Explain current code
- **"fix"** - Suggest fixes for errors
- **"optimize"** - Optimize the current code
- **"document"** - Generate documentation
- **"test"** - Generate test cases
- **"refactor"** - Suggest refactoring
- **"debug"** - Help debug issues

### Keyboard Shortcuts
- **`Ctrl+Shift+C`** - Activate copilot
- **`Ctrl+Shift+O`** - Toggle overlay
- **`Escape`** - Close overlay

### Features
- **Screen Monitoring**: Watches your screen for code and errors
- **Real-time Suggestions**: Provides instant AI-powered suggestions
- **Invisible Overlay**: Non-intrusive interface
- **Voice Control**: Natural language interaction
- **Multi-language Support**: Python, JavaScript, TypeScript, Java, C++, HTML, CSS, and more

## 🐛 Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**"Tesseract not found"**
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

**"OpenAI API key not set"**
- Make sure you have a `.env` file with your API key
- Get an API key from: https://platform.openai.com/api-keys

**Audio not working**
- Check microphone permissions
- Try different audio devices in config
- Test with: `python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"`

### Getting Help

1. **Check the logs:**
   ```bash
   tail -f copilot.log
   ```

2. **Run with debug mode:**
   - Edit `config.py`
   - Set `ENABLE_DEBUG_MODE = True`

3. **Test individual components:**
   ```bash
   python -c "from screen_monitor import ScreenMonitor; print('Screen monitor OK')"
   python -c "from audio_processor import AudioProcessor; print('Audio processor OK')"
   ```

## 🎨 Customization

### Configuration Options

Edit `config.py` to customize:

```python
# Audio Settings
HOTWORD_PHRASE = "hey copilot"
HOTWORD_SENSITIVITY = 0.8

# Screen Monitoring
SCREEN_CAPTURE_INTERVAL = 2.0  # seconds
OCR_ENABLED = True

# UI Settings
OVERLAY_POSITION = "top-right"  # top-right, top-left, bottom-right, bottom-left
OVERLAY_OPACITY = 0.9

# AI Settings
OPENAI_MODEL = "gpt-4"
MAX_TOKENS = 1000
```

### Custom Voice Commands
```python
# In config.py
VOICE_COMMANDS = {
    "explain": "Explain the current code",
    "fix": "Suggest fixes for errors",
    "optimize": "Optimize the current code",
    "custom": "Your custom command",  # Add your own
}
```

## 📊 Performance Tips

- **Reduce screen capture frequency** for better performance
- **Disable OCR** if not needed: `OCR_ENABLED = False`
- **Use caching** for repeated suggestions: `ENABLE_CACHING = True`
- **Limit context window** for faster processing

## 🔒 Security

- API keys are stored locally in `.env` file
- No code is sent to external services except OpenAI
- Screen capture is processed locally
- Audio is processed locally for hotword detection

## 📈 Advanced Usage

### Integration with IDEs
The copilot works alongside any IDE or text editor. It monitors your screen and provides suggestions regardless of what you're using.

### Batch Processing
```python
# Process multiple files
from ai_engine import AIEngine

ai = AIEngine()
for file in files:
    with open(file, 'r') as f:
        code = f.read()
    suggestions = ai.analyze_code_quality(code, language="python")
    print(f"Suggestions for {file}:", suggestions)
```

### Custom AI Prompts
```python
# In ai_engine.py, modify _build_prompt method
def _build_prompt(self, context, command=None, query=None):
    # Add your custom prompt engineering here
    pass
```

## 🚀 Next Steps

1. **Explore the codebase**: Check out the individual modules
2. **Customize for your workflow**: Modify config and add custom commands
3. **Integrate with your tools**: Connect with your favorite IDEs
4. **Contribute**: Add new features and improvements

Happy coding! 🎉 