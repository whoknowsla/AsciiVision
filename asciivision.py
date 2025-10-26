#!/usr/bin/env python3
"""
AsciiVision - Convert ASCII art to images and images to ASCII art
with accessibility features and automatic screen reader detection.
"""

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

import keyring
import psutil
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI

# For secure input
try:
    import getpass
except ImportError:
    getpass = None


class AsciiVision:
    """Main AsciiVision application class."""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
        self.client = None
        
    def _get_config_dir(self) -> Path:
        """Get the appropriate config directory for the current OS."""
        system = platform.system()
        
        if system == "Windows":
            config_dir = Path(os.environ.get("APPDATA", "")) / "AsciiVision"
        elif system == "Darwin":  # macOS
            config_dir = Path.home() / "Library" / "Application Support" / "AsciiVision"
        else:  # Linux and others
            config_dir = Path.home() / ".config" / "asciivision"
            
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        default_config = {
            "auto_describe": False,
            "screen_reader": None,
            "model": "gpt-4o"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except (json.JSONDecodeError, IOError):
                pass
                
        return default_config
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save config: {e}")
    
    def _detect_environment(self) -> str:
        """Detect if running in container, CI/CD, or headless environment."""
        # Check for container
        if Path("/.dockerenv").exists():
            return "container"
            
        # Check for CI/CD environment
        if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
            return "ci"
            
        # Check for headless (no display)
        if platform.system() != "Windows" and not os.environ.get("DISPLAY"):
            return "headless"
            
        return "desktop"
    
    def _detect_screen_reader(self) -> Optional[str]:
        """Detect if a screen reader is running."""
        system = platform.system()
        
        if system == "Linux":
            # Check for Orca, speech-dispatcher, or DBus service
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    name = proc.info['name'].lower()
                    if any(sr in name for sr in ['orca', 'speech-dispatcher']):
                        return "Orca"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            # Check DBus service
            try:
                result = subprocess.run(['dbus-send', '--session', '--dest=org.gnome.Orca', 
                                      '--type=method_call', '--print-reply', 
                                      '/org/gnome/Orca', 'org.gnome.Orca.GetVersion'],
                                     capture_output=True, timeout=2)
                if result.returncode == 0:
                    return "Orca"
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
                
        elif system == "Darwin":  # macOS
            # Check for VoiceOver
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] == "VoiceOver":
                        return "VoiceOver"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        elif system == "Windows":
            # Check for NVDA, JAWS
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name'].lower()
                    if name in ['nvda.exe', 'jfw.exe', 'jaws.exe']:
                        return "NVDA" if name == 'nvda.exe' else "JAWS"
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        return None
    
    def _get_api_key(self) -> Optional[str]:
        """Get OpenAI API key from keyring or .env file."""
        # Try keyring first (unless in container/CI/headless)
        environment = self._detect_environment()
        if environment == "desktop":
            try:
                key = keyring.get_password("asciivision", "openai_api_key")
                if key:
                    return key
            except Exception:
                pass
        
        # Fallback to .env file
        load_dotenv()
        return os.getenv("OPENAI_API_KEY")
    
    def _setup_openai_client(self) -> bool:
        """Set up OpenAI client with API key."""
        api_key = self._get_api_key()
        if not api_key:
            # Prompt user for API key
            api_key = self._prompt_for_api_key()
            if not api_key:
                print("Error: OpenAI API key required for image descriptions.")
                return False
            
            # Save the API key securely
            self._save_api_key(api_key)
            
        self.client = OpenAI(api_key=api_key)
        return True
    
    def _save_api_key(self, api_key: str):
        """Save API key securely to keyring or .env file."""
        environment = self._detect_environment()
        
        # Try keyring first (unless in container/CI/headless)
        if environment == "desktop":
            try:
                keyring.set_password("asciivision", "openai_api_key", api_key)
                print("✓ API key saved securely to keyring!")
                return
            except Exception as e:
                print(f"Warning: Could not save to keyring: {e}")
                print("Falling back to .env file...")
        
        # Fallback to .env file
        try:
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print("✓ API key saved to .env file!")
        except Exception as e:
            print(f"Error: Could not save API key: {e}")
    
    def _ask_for_auto_describe(self, screen_reader: str) -> bool:
        """Ask user if they want to enable automatic descriptions."""
        print(f"\nScreen reader detected ({screen_reader}). Enable automatic image descriptions? [y/n]")
        try:
            response = input().lower().strip()
            return response in ['y', 'yes']
        except (EOFError, KeyboardInterrupt):
            return False
    
    def _secure_input(self, prompt: str) -> str:
        """Get secure input (password-like) from user."""
        if getpass:
            return getpass.getpass(prompt)
        else:
            # Fallback for systems without getpass
            print(prompt, end='', flush=True)
            import msvcrt
            password = ""
            while True:
                char = msvcrt.getch()
                if char in [b'\r', b'\n']:  # Enter key
                    print()
                    break
                elif char == b'\x08':  # Backspace
                    if password:
                        password = password[:-1]
                        print('\b \b', end='', flush=True)
                else:
                    password += char.decode('utf-8', errors='ignore')
                    print('*', end='', flush=True)
            return password
    
    def _mask_api_key(self, api_key: str) -> str:
        """Mask API key showing only first and last 4 characters."""
        if len(api_key) <= 8:
            return '*' * len(api_key)
        return api_key[:4] + '*' * (len(api_key) - 8) + api_key[-4:]
    
    def _prompt_for_api_key(self) -> Optional[str]:
        """Prompt user for API key with secure input and confirmation."""
        print("\nOpenAI API Key Setup")
        print("===================")
        print("To enable automatic image descriptions, you need an OpenAI API key.")
        print("You can get one from: https://platform.openai.com/api-keys")
        print()
        
        # Get API key with secure input
        api_key = self._secure_input("Enter your OpenAI API key: ")
        
        if not api_key.strip():
            print("No API key provided. Skipping setup.")
            return None
        
        # Confirm the key immediately after input
        masked_key = self._mask_api_key(api_key)
        print(f"\nIs this your API key: {masked_key}? [y/n]")
        
        try:
            response = input().lower().strip()
            if response in ['y', 'yes']:
                print("✓ API key confirmed!")
                return api_key.strip()
            else:
                print("API key not confirmed. Skipping setup.")
                return None
        except (EOFError, KeyboardInterrupt):
            print("\nAPI key setup cancelled.")
            return None
    
    def _describe_image(self, image_path: str, model: str = None) -> Optional[str]:
        """Generate description of an image using GPT-4o vision."""
        if not self.client:
            if not self._setup_openai_client():
                return None
                
        model = model or self.config.get("model", "gpt-4o")
        
        try:
            import base64
            
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "This is ASCII art converted to an image. Please describe it for someone who is visually impaired. Your description should help them understand what the ASCII art represents:\n\n1. **If it contains text**: Read the letters/words clearly and spell them out\n2. **If it's an object/scene**: Describe what it shows in detail\n3. **Character details**: Explain what specific ASCII characters are used (like | for lines, o for eyes, ^ for ears, etc.)\n4. **Layout and structure**: Describe how the characters are arranged\n\nFocus on being descriptive and helpful for someone who cannot see the image. Be specific about the visual elements and what they represent."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_data}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=300
                )
                
            return response.choices[0].message.content
            
        except Exception as e:
            error_msg = str(e)
            # Check if it's an API error vs other error
            if "api.openai.com" in error_msg or "OpenAI" in error_msg:
                print(f"Error generating description: API request failed")
            else:
                print(f"Error generating description: {error_msg}")
            return None
    
    def ascii_to_image(self, ascii_text: str, output_path: str, 
                      font_name: str = "Courier", font_size: int = 12,
                      bg_color: str = "white", fg_color: str = "black",
                      padding: int = 20, spacing: int = 1,
                      antialias: bool = True, wrap_width: int = 80) -> bool:
        """Convert ASCII text to image."""
        try:
            # Wrap text if needed
            if wrap_width > 0:
                lines = []
                for line in ascii_text.split('\n'):
                    if len(line) <= wrap_width:
                        lines.append(line)
                    else:
                        # Simple word wrapping
                        words = line.split()
                        current_line = ""
                        for word in words:
                            if len(current_line + word) <= wrap_width:
                                current_line += word + " "
                            else:
                                if current_line:
                                    lines.append(current_line.rstrip())
                                current_line = word + " "
                        if current_line:
                            lines.append(current_line.rstrip())
                ascii_text = '\n'.join(lines)
            
            # Calculate image dimensions
            lines = ascii_text.split('\n')
            max_width = max(len(line) for line in lines) if lines else 0
            
            # Load font
            try:
                font = ImageFont.truetype(font_name, font_size)
            except OSError:
                # Fallback to default font
                font = ImageFont.load_default()
            
            # Get text dimensions
            bbox = font.getbbox(ascii_text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate image size with padding
            img_width = text_width + (padding * 2)
            img_height = text_height + (padding * 2)
            
            # Create image
            image = Image.new('RGB', (img_width, img_height), bg_color)
            draw = ImageDraw.Draw(image)
            
            # Draw text
            draw.text((padding, padding), ascii_text, font=font, fill=fg_color)
            
            # Save image
            image.save(output_path)
            return True
            
        except Exception as e:
            print(f"Error converting ASCII to image: {e}")
            return False
    
    def image_to_ascii(self, image_path: str, width: int = 100) -> str:
        """Convert image to ASCII art."""
        try:
            # ASCII characters ordered by brightness
            ascii_chars = "@%#*+=-:. "
            
            # Load and process image
            image = Image.open(image_path)
            
            # Convert to grayscale
            image = image.convert('L')
            
            # Calculate new dimensions preserving aspect ratio
            aspect_ratio = image.height / image.width
            height = int(width * aspect_ratio * 0.55)  # Adjust for character aspect ratio
            
            # Resize image
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            
            # Convert to ASCII
            pixels = image.getdata()
            ascii_text = ""
            
            for i, pixel in enumerate(pixels):
                # Map pixel brightness to ASCII character
                char_index = int((pixel / 255) * (len(ascii_chars) - 1))
                ascii_text += ascii_chars[char_index]
                
                # Add newline at end of each row
                if (i + 1) % width == 0:
                    ascii_text += '\n'
            
            return ascii_text
            
        except Exception as e:
            print(f"Error converting image to ASCII: {e}")
            return ""


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AsciiVision - Convert ASCII art to images and images to ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python asciivision.py -i art.txt -o out.jpg          # ASCII → Image
  python asciivision.py -a -i photo.png -w 100 > out.txt  # Image → ASCII
  python asciivision.py -i art.txt -o out.jpg -d         # Force description
  python asciivision.py -D -m gpt-4o-mini                # Describe only existing image
        """
    )
    
    # Input/Output
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    
    # Conversion modes
    parser.add_argument('-a', '--to-ascii', action='store_true', 
                       help='Convert image to ASCII (default: ASCII to image)')
    
    # ASCII to Image options
    parser.add_argument('--font', default='Courier', help='Font name (default: Courier)')
    parser.add_argument('--font-size', type=int, default=12, help='Font size (default: 12)')
    parser.add_argument('--bg', default='white', help='Background color (default: white)')
    parser.add_argument('--fg', default='black', help='Foreground color (default: black)')
    parser.add_argument('--padding', type=int, default=20, help='Padding in pixels (default: 20)')
    parser.add_argument('--spacing', type=int, default=1, help='Line spacing (default: 1)')
    parser.add_argument('--antialias', action='store_true', help='Enable antialiasing')
    parser.add_argument('--wrap', type=int, default=80, help='Wrap width (default: 80)')
    
    # Image to ASCII options
    parser.add_argument('-w', '--width', type=int, default=100, 
                       help='ASCII width in characters (default: 100)')
    
    # Description options
    parser.add_argument('-d', '--auto-describe', action='store_true',
                       help='Force automatic description')
    parser.add_argument('-D', '--describe-only', action='store_true',
                       help='Describe existing image only')
    parser.add_argument('-m', '--model', default='gpt-4o',
                       help='OpenAI model for descriptions (default: gpt-4o)')
    
    args = parser.parse_args()
    
    # Initialize AsciiVision
    app = AsciiVision()
    
    # Handle describe-only mode
    if args.describe_only:
        if not args.input:
            print("Error: Input file required for describe-only mode")
            sys.exit(1)
            
        description = app._describe_image(args.input, args.model)
        if description:
            print(f"\nImage Description:\n{description}")
        sys.exit(0)
    
    # Check for screen reader and ask about auto-description
    screen_reader = app._detect_screen_reader()
    if screen_reader and not app.config.get("screen_reader"):
        app.config["screen_reader"] = screen_reader
        if app._ask_for_auto_describe(screen_reader):
            app.config["auto_describe"] = True
            app._save_config()
    
    # Read input file (only for ASCII to image conversion)
    input_content = None
    if not args.to_ascii:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                input_content = f.read()
        except FileNotFoundError:
            print(f"Error: Input file '{args.input}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)
    
    # Perform conversion
    if args.to_ascii:
        # Image to ASCII
        ascii_text = app.image_to_ascii(args.input, args.width)
        if ascii_text:
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(ascii_text)
                print(f"ASCII art saved to {args.output}")
            else:
                print(ascii_text)
                
            # Auto-describe if enabled
            if (app.config.get("auto_describe") or args.auto_describe) and args.input:
                description = app._describe_image(args.input, args.model)
                if description:
                    print(f"\nImage Description:\n{description}")
    else:
        # ASCII to Image
        if not args.output:
            print("Error: Output file required for ASCII to image conversion")
            sys.exit(1)
            
        success = app.ascii_to_image(
            input_content, args.output,
            font_name=args.font, font_size=args.font_size,
            bg_color=args.bg, fg_color=args.fg,
            padding=args.padding, spacing=args.spacing,
            antialias=args.antialias, wrap_width=args.wrap
        )
        
        if success:
            print(f"Image saved to {args.output}")
            
            # Auto-describe if enabled
            if (app.config.get("auto_describe") or args.auto_describe) and args.output:
                description = app._describe_image(args.output, args.model)
                if description:
                    print(f"\nImage Description:\n{description}")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
