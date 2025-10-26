# AsciiVision 🎨

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple.svg)](https://openai.com)

**Convert ASCII art to images and images to ASCII art with AI-powered accessibility features**

AsciiVision is a powerful command-line tool that bridges the gap between ASCII art and visual content, with built-in accessibility features powered by OpenAI's GPT-4o vision model. It automatically detects screen readers and provides intelligent image descriptions for visually impaired users.

## ✨ Features

### 🔄 **Dual Conversion**
- **ASCII → Image**: Convert text-based ASCII art to PNG/JPG images with custom styling
- **Image → ASCII**: Transform any image into ASCII art using brightness mapping

### ♿ **Accessibility First**
- **Auto Screen Reader Detection**: Supports NVDA, JAWS, Orca, VoiceOver, and more
- **AI-Powered Descriptions**: GPT-4o vision generates detailed image descriptions
- **Secure API Key Management**: Password-like input with confirmation display
- **Screen Reader Friendly**: All outputs optimized for accessibility tools

### 🎨 **Customization**
- **Font Control**: Choose fonts, sizes, and styling
- **Color Themes**: Custom background and foreground colors
- **Layout Options**: Adjustable padding, spacing, and wrapping
- **Antialiasing**: High-quality image rendering

### 🔒 **Security & Storage**
- **OS Keychain Integration**: Secure API key storage using system keyring
- **Environment Detection**: Smart fallbacks for containers and CI/CD
- **Configuration Management**: Persistent user preferences

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AsciiVision.git
cd AsciiVision
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up OpenAI API key** (optional, for image descriptions)
```bash
# The tool will prompt you securely when needed
python asciivision.py -D -i any_image.png
```

### Basic Usage

**Convert ASCII art to image:**
```bash
python asciivision.py -i examples/hello.txt -o hello.png
```

**Convert image to ASCII art:**
```bash
python asciivision.py -a -i photo.jpg -w 80 -o ascii_art.txt
```

**Generate AI descriptions:**
```bash
python asciivision.py -i art.txt -o image.png -d
```

## 📖 Detailed Usage

### Command Line Options

#### **Input/Output**
- `-i, --input FILE`: Input file path (required)
- `-o, --output FILE`: Output file path

#### **Conversion Modes**
- `-a, --to-ascii`: Convert image to ASCII (default: ASCII to image)

#### **ASCII to Image Options**
- `--font NAME`: Font name (default: Courier)
- `--font-size SIZE`: Font size in pixels (default: 12)
- `--bg COLOR`: Background color (default: white)
- `--fg COLOR`: Foreground color (default: black)
- `--padding PIXELS`: Padding around text (default: 20)
- `--spacing VALUE`: Line spacing multiplier (default: 1)
- `--antialias`: Enable antialiasing for smoother text
- `--wrap WIDTH`: Text wrapping width (default: 80)

#### **Image to ASCII Options**
- `-w, --width CHARS`: ASCII art width in characters (default: 100)

#### **AI Description Options**
- `-d, --auto-describe`: Force automatic description generation
- `-D, --describe-only`: Describe existing image only
- `-m, --model MODEL`: OpenAI model for descriptions (default: gpt-4o)

## 🎯 Examples

### **Basic ASCII Art Conversion**

Create a simple ASCII art file (`cat.txt`):
```
    /\_/\  
   (  o.o  ) 
    > ^ <
    
   /\     /\
  /  \   /  \
 /    \ /    \
/______\______\
```

Convert to image:
```bash
python asciivision.py -i cat.txt -o cat.png
```

### **Custom Styling**

```bash
python asciivision.py -i art.txt -o styled.png \
  --font "Arial" \
  --font-size 16 \
  --bg "#f0f8ff" \
  --fg "#2c3e50" \
  --padding 30 \
  --antialias
```

### **Image to ASCII Conversion**

```bash
python asciivision.py -a -i photo.jpg -w 120 -o photo_ascii.txt
```

### **AI-Powered Descriptions**

```bash
# Generate description during conversion
python asciivision.py -i art.txt -o image.png -d

# Describe existing image
python asciivision.py -D -i existing_image.png
```

## ♿ Accessibility Features

### **Automatic Screen Reader Detection**

AsciiVision automatically detects and supports:
- **Windows**: NVDA, JAWS
- **macOS**: VoiceOver
- **Linux**: Orca, speech-dispatcher, DBus services

When detected, you'll see:
```
Screen reader detected (NVDA). Enable automatic image descriptions? [y/n]
```

### **AI-Powered Image Descriptions**

When enabled, AsciiVision generates detailed descriptions like:
```
Image Description:
This ASCII art represents a simple face of a character, likely an animal, with a cute expression.

1. **Ears**: The ears are depicted using the "^" character, forming two small triangles...
2. **Eyes and Nose**: The eyes are created using the lowercase "o" characters...
3. **Overall Structure**: The characters are arranged to form the top of the character...
```

### **Secure API Key Setup**

The tool provides a secure, password-like input for API keys:
```
OpenAI API Key Setup
===================
To enable automatic image descriptions, you need an OpenAI API key.
You can get one from: https://platform.openai.com/api-keys

Enter your OpenAI API key: [hidden input]
Is this your API key: sk-1********************************cdef? [y/n]
✓ API key confirmed!
✓ API key saved securely to keyring!
```

## ⚙️ Configuration

### **Config File Locations**
- **Linux**: `~/.config/asciivision/config.json`
- **macOS**: `~/Library/Application Support/AsciiVision/config.json`
- **Windows**: `%APPDATA%\AsciiVision\config.json`

### **Configuration Options**
```json
{
  "auto_describe": true,
  "screen_reader": "NVDA",
  "model": "gpt-4o"
}
```

### **Environment Detection**

AsciiVision automatically adapts to different environments:
- **Desktop**: Uses OS keychain for secure storage
- **Container**: Falls back to `.env` file storage
- **CI/CD**: Uses environment variables
- **Headless**: Disables interactive features

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_asciivision.py
```

Test examples:
```bash
python examples/demo.py
```

## 📦 Dependencies

- **[Pillow](https://pillow.readthedocs.io/)**: Image processing and manipulation
- **[keyring](https://pypi.org/project/keyring/)**: Secure credential storage
- **[python-dotenv](https://pypi.org/project/python-dotenv/)**: Environment variable management
- **[OpenAI](https://openai.com/)**: GPT-4o vision API for image descriptions
- **[psutil](https://pypi.org/project/psutil/)**: Process detection for screen readers

## 🤝 Contributing

AsciiVision is built with inclusivity in mind. We welcome contributions that maintain or improve accessibility standards.

### **Development Setup**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python test_asciivision.py`
5. Submit a pull request

### **Accessibility Guidelines**
- Ensure all new features work with screen readers
- Test with different screen reader software
- Maintain clear, descriptive error messages
- Keep command-line output screen-reader friendly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4o vision capabilities
- The accessibility community for feedback and testing
- Contributors who help make technology more inclusive

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/AsciiVision/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AsciiVision/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/AsciiVision/wiki)

---

**Made with ❤️ for accessibility and inclusivity**