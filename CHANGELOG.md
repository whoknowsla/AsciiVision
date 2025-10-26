# Changelog

All notable changes to AsciiVision will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with 4 test cases
- Secure API key input with password-like masking
- API key confirmation with masked display (shows first/last 4 characters)
- Improved AI prompts for better ASCII art descriptions
- Accessibility-focused image descriptions for visually impaired users
- Windows console encoding fixes for Unicode support
- Comprehensive README with badges and examples
- Contributing guidelines and development documentation
- Git ignore file for proper version control

### Changed
- Enhanced error handling for API requests
- Improved prompt structure for AI descriptions
- Better organization of command-line options
- More detailed accessibility descriptions

### Fixed
- Unicode encoding issues on Windows console
- API key corruption in keyring storage
- Raw string warnings in ASCII art examples
- Error handling for invalid API keys

## [1.0.0] - 2025-10-26

### Added
- Initial release of AsciiVision
- ASCII art to image conversion
- Image to ASCII art conversion
- Automatic screen reader detection (NVDA, JAWS, Orca, VoiceOver)
- GPT-4o powered image descriptions
- Secure API key storage using OS keychain
- Configuration management
- Cross-platform support (Windows, macOS, Linux)
- Environment detection (desktop, container, CI/CD)
- Customizable font, color, and layout options
- Command-line interface with comprehensive options
- Example files and demo scripts

### Features
- **Conversion**: Bidirectional ASCII ↔ Image conversion
- **Accessibility**: Screen reader detection and AI descriptions
- **Security**: Secure key storage with fallback options
- **Customization**: Font, color, size, and layout controls
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Environment-aware**: Adapts to different deployment scenarios

### Technical Details
- Python 3.8+ support
- Pillow for image processing
- OpenAI GPT-4o for vision capabilities
- Keyring for secure credential storage
- psutil for process detection
- python-dotenv for environment management
