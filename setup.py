#!/usr/bin/env python3
"""
Setup script for AsciiVision.
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False

def setup_api_key():
    """Guide user through API key setup."""
    print("\nOpenAI API Key Setup")
    print("===================")
    print("To enable automatic image descriptions, you need an OpenAI API key.")
    print("You can get one from: https://platform.openai.com/api-keys")
    print()
    
    choice = input("Do you want to set up your API key now? [y/n]: ").lower().strip()
    
    if choice in ['y', 'yes']:
        api_key = input("Enter your OpenAI API key: ").strip()
        
        if api_key:
            try:
                import keyring
                keyring.set_password("asciivision", "openai_api_key", api_key)
                print("✓ API key saved securely to keyring!")
                return True
            except Exception as e:
                print(f"✗ Failed to save to keyring: {e}")
                print("Falling back to .env file...")
                
                with open(".env", "w") as f:
                    f.write(f"OPENAI_API_KEY={api_key}\n")
                print("✓ API key saved to .env file!")
                return True
        else:
            print("No API key provided. You can set it up later.")
    else:
        print("Skipping API key setup. You can set it up later.")
    
    return True

def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    try:
        subprocess.check_call([sys.executable, "test_asciivision.py"])
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Some tests failed, but the basic functionality should work.")
        return False

def main():
    """Main setup function."""
    print("AsciiVision Setup")
    print("=================")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup API key
    setup_api_key()
    
    # Run tests
    run_tests()
    
    print("\n🎉 Setup complete!")
    print("\nQuick start:")
    print("1. Create an ASCII art file (e.g., examples/hello.txt)")
    print("2. Convert to image: python asciivision.py -i examples/hello.txt -o output.png")
    print("3. Convert image to ASCII: python asciivision.py -a -i output.png -w 80")
    print("\nFor more examples, see the README.md file.")

if __name__ == "__main__":
    main()
