#!/usr/bin/env python3
"""
Example script demonstrating AsciiVision functionality.
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Add the parent directory to the path so we can import asciivision
sys.path.insert(0, str(Path(__file__).parent.parent))

from asciivision import AsciiVision

def main():
    """Run example conversions."""
    app = AsciiVision()
    
    # Get the examples directory
    examples_dir = Path(__file__).parent
    hello_file = examples_dir / "hello.txt"
    cat_file = examples_dir / "cat.txt"
    
    print("AsciiVision Examples")
    print("===================")
    
    # Example 1: Convert hello.txt to image
    if hello_file.exists():
        print(f"\n1. Converting {hello_file.name} to image...")
        success = app.ascii_to_image(
            hello_file.read_text(encoding='utf-8'),
            examples_dir / "hello_output.png",
            font_size=16,
            bg_color="white",
            fg_color="black",
            padding=30
        )
        if success:
            print("✓ Successfully created hello_output.png")
        else:
            print("✗ Failed to create hello_output.png")
    
    # Example 2: Convert cat.txt to image with custom styling
    if cat_file.exists():
        print(f"\n2. Converting {cat_file.name} to image with custom styling...")
        success = app.ascii_to_image(
            cat_file.read_text(encoding='utf-8'),
            examples_dir / "cat_output.png",
            font_name="Courier New",
            font_size=14,
            bg_color="#f0f8ff",
            fg_color="#2c3e50",
            padding=25
        )
        if success:
            print("✓ Successfully created cat_output.png")
        else:
            print("✗ Failed to create cat_output.png")
    
    print("\nExamples completed!")
    print("\nTo test image-to-ASCII conversion, you can:")
    print("1. Create a simple image file")
    print("2. Run: python asciivision.py -a -i your_image.png -w 80")

if __name__ == "__main__":
    main()
