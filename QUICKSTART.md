# 🚀 Quick Start Guide

Get your Real-Time Overlay Copilot up and running in minutes!

## ⚡ Super Quick Start

1. **Clone and Setup**:
   ```bash
   git clone <repository-url>
   cd AI-Overlay-Copilot
   python setup.py
   ```

2. **Add API Key**:
   ```bash
   # Edit .env file and add your OpenAI API key
   nano .env
   ```

3. **Run the Copilot**:
   ```bash
   python main.py
   ```

4. **Activate**:
   - Say "Hey Copilot" 
   - Or press `Ctrl+Shift+C`

That's it! 🎉

## 🎯 Try the Demo First

Want to see what it can do without full setup?

```bash
python demo.py
```

This shows the copilot's capabilities with sample code and suggestions.

## 🔧 Full Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- macOS/Linux/Windows

### Step-by-Step Setup

1. **Install System Dependencies**:

   **macOS**:
   ```bash
   brew install tesseract portaudio
   ```

   **Ubuntu/Debian**:
   ```bash
   sudo apt-get install tesseract-ocr portaudio19-dev python3-tk
   ```

   **Windows**:
   - Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
   - Download PortAudio from: http://www.portaudio.com/download.html

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   ```bash
   cp env_example.txt .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run Setup Script**:
   ```bash
   python setup.py
   ```

## 🎮 Usage

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

## 🛠️ Configuration

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

## 🐛 Troubleshooting

### Common Issues

**"No module named 'pyaudio'"**:
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**"Tesseract not found"**:
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

**"OpenAI API key not set"**:
- Make sure you have a `.env` file with your API key
- Get an API key from: https://platform.openai.com/api-keys

**Audio not working**:
- Check microphone permissions
- Try different audio devices in config
- Test with: `python -c "import pyaudio; print(pyaudio.PyAudio().get_device_count())"`

### Getting Help

1. Check the logs in `copilot.log`
2. Run with debug mode: Set `ENABLE_DEBUG_MODE = True` in config
3. Test individual components:
   ```bash
   python -c "from screen_monitor import ScreenMonitor; print('Screen monitor OK')"
   python -c "from audio_processor import AudioProcessor; print('Audio processor OK')"
   ```

## 🎨 Customization

### Custom Hotwords
```python
# In config.py
HOTWORD_PHRASE = "computer"  # Change to your preferred phrase
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

### Custom File Types
```python
# In config.py
MONITORED_EXTENSIONS = [
    ".py", ".js", ".ts", ".java", ".cpp", ".c", ".cs",
    ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".scala",
    ".html", ".css", ".scss", ".sass", ".json", ".xml",
    ".yaml", ".yml", ".your_extension"  # Add your own
]
```

## 🚀 Advanced Usage

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

## 📈 Next Steps

1. **Explore the codebase**: Check out the individual modules
2. **Customize for your workflow**: Modify config and add custom commands
3. **Integrate with your tools**: Connect with your favorite IDEs
4. **Contribute**: Add new features and improvements

Happy coding! 🎉 