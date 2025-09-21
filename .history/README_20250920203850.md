# 🚀 Real-Time Overlay Copilot

A screen-aware AI coding copilot that provides real-time assistance for developers by monitoring your screen, listening to audio, and suggesting relevant code snippets, bug fixes, and context-aware solutions.

## ✨ Features

- **🔍 Screen Monitoring**: Watches your screen in real-time to understand context
- **🎤 Audio Processing**: Listens for hotwords and voice commands
- **🤖 AI-Powered Suggestions**: Provides relevant code snippets and bug fixes
- **👻 Invisible Overlay**: Non-intrusive interface that appears when needed
- **⚡ Hotword Activation**: "Hey Copilot" to activate assistance
- **📝 Context Awareness**: Understands your current coding environment
- **🔧 Real-Time Fixes**: Suggests immediate solutions to problems

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-Overlay-Copilot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Install system dependencies:
```bash
# macOS
brew install tesseract portaudio

# Ubuntu/Debian
sudo apt-get install tesseract-ocr portaudio19-dev
```

## 🚀 Usage

### **One-Command Options**

#### **Smart Launcher (Recommended)**
```bash
python run_copilot.py
```
Choose from:
- 🎯 **Demo** (no setup required)
- 🚀 **Full Copilot** (requires OpenAI API key)
- 💰 **Free Copilot** (no API costs - rule-based)
- 🔧 **Setup only**

#### **Direct Commands**
```bash
# Free version (no API costs)
python free_copilot.py

# Demo version (no setup required)
python demo.py

# Full version (requires OpenAI API key)
python main.py
```

### **Cost Options**
- **💰 FREE**: Rule-based analysis, no API costs
- **🆓 FREE**: Open source LLMs (Ollama, Hugging Face)
- **💵 Affordable**: GPT-3.5-turbo (~$1-10/month)
- **💎 Premium**: GPT-4 (~$10-50/month)

See [COST_GUIDE.md](COST_GUIDE.md) for detailed pricing and [OPEN_SOURCE_GUIDE.md](OPEN_SOURCE_GUIDE.md) for open source options.

## 🏗️ Architecture

- **Screen Monitor**: Captures and analyzes screen content
- **Audio Processor**: Handles hotword detection and voice commands
- **AI Engine**: Processes context and generates suggestions
- **Overlay UI**: Displays suggestions in a non-intrusive way
- **Context Manager**: Maintains awareness of current development state

## 🔧 Configuration

Edit `config.py` to customize:
- Hotword sensitivity
- Screen capture frequency
- AI model preferences
- UI appearance
- Keyboard shortcuts

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines. 