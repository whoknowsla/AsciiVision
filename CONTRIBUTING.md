# Contributing to AsciiVision

Thank you for your interest in contributing to AsciiVision! This project is built with accessibility and inclusivity in mind, and we welcome contributions that maintain or improve these standards.

## 🎯 Development Philosophy

AsciiVision prioritizes:
- **Accessibility**: All features must work with screen readers
- **Inclusivity**: Making technology accessible to everyone
- **Security**: Secure handling of API keys and user data
- **Simplicity**: Clear, intuitive command-line interface

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic understanding of accessibility principles

### Setup Development Environment

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/AsciiVision.git
cd AsciiVision
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run tests**
```bash
python test_asciivision.py
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python test_asciivision.py

# Run examples
python examples/demo.py

# Test specific functionality
python asciivision.py --help
```

### Test Coverage
Ensure your changes are tested for:
- ✅ ASCII to image conversion
- ✅ Image to ASCII conversion
- ✅ Screen reader detection
- ✅ API key management
- ✅ Configuration handling
- ✅ Error scenarios

## 📝 Making Changes

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions
- Keep functions focused and small

### Accessibility Guidelines
- Test with screen readers (NVDA, JAWS, Orca, VoiceOver)
- Ensure all output is screen-reader friendly
- Provide clear error messages
- Use semantic markup where applicable

### Security Considerations
- Never log or expose API keys
- Use secure input methods for sensitive data
- Validate all user inputs
- Follow secure coding practices

## 🔧 Feature Development

### Adding New Features
1. **Plan**: Consider accessibility implications
2. **Design**: Ensure screen reader compatibility
3. **Implement**: Follow existing code patterns
4. **Test**: Verify with accessibility tools
5. **Document**: Update README and help text

### Common Patterns

**Adding a new command-line option:**
```python
parser.add_argument('--new-option', action='store_true',
                   help='Description of the new option')
```

**Adding configuration:**
```python
default_config = {
    "auto_describe": False,
    "screen_reader": None,
    "model": "gpt-4o",
    "new_setting": "default_value"  # Add here
}
```

**Error handling:**
```python
try:
    # Your code here
    pass
except Exception as e:
    print(f"Error: {e}")
    return False
```

## 🐛 Bug Reports

When reporting bugs, please include:
- **Environment**: OS, Python version, screen reader (if applicable)
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Error messages**: Full error output
- **Accessibility impact**: How it affects screen reader users

## 💡 Feature Requests

We welcome feature requests that:
- Improve accessibility
- Enhance user experience
- Add new conversion options
- Improve security
- Support additional platforms

## 📋 Pull Request Process

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Accessibility features tested with screen readers
- [ ] Documentation updated
- [ ] No sensitive data exposed

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Accessibility Testing
- [ ] Tested with NVDA (Windows)
- [ ] Tested with JAWS (Windows)
- [ ] Tested with Orca (Linux)
- [ ] Tested with VoiceOver (macOS)

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
```

## 🏷️ Release Process

Releases follow semantic versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on accessibility and inclusion

### Communication
- Use clear, descriptive commit messages
- Provide helpful code comments
- Be patient with questions
- Share knowledge and best practices

## 📚 Resources

### Accessibility Testing
- [WebAIM Screen Reader Testing](https://webaim.org/articles/screenreader_testing/)
- [NVDA Documentation](https://www.nvaccess.org/about-nvda/)
- [JAWS Documentation](https://www.freedomscientific.com/products/software/jaws/)
- [Orca Documentation](https://help.gnome.org/users/orca/)

### Development Tools
- [Python Accessibility Guidelines](https://accessibility.18f.gov/python/)
- [WCAG Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Screen Reader Testing Checklist](https://webaim.org/articles/screenreader_testing/)

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/AsciiVision/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/AsciiVision/discussions)
- **Email**: [Your email here]

---

Thank you for contributing to making technology more accessible! 🌟
