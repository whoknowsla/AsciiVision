#!/usr/bin/env python3
"""
Test script for AsciiVision functionality.
"""

import os
import sys
from pathlib import Path

# Fix Windows console encoding issues
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def test_ascii_to_image():
    """Test ASCII to image conversion."""
    print("Testing ASCII to Image conversion...")
    
    # Simple ASCII art
    ascii_art = r"""
    /\_/\  
   (  o.o  ) 
    > ^ <
    
   /\     /\
  /  \   /  \
 /    \ /    \
/______\______\
"""
    
    try:
        from asciivision import AsciiVision
        app = AsciiVision()
        
        success = app.ascii_to_image(
            ascii_art.strip(),
            "test_output.png",
            font_size=14,
            bg_color="white",
            fg_color="black",
            padding=20
        )
        
        if success and Path("test_output.png").exists():
            print("✓ ASCII to Image conversion successful!")
            return True
        else:
            print("✗ ASCII to Image conversion failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error during ASCII to Image test: {e}")
        return False

def test_image_to_ascii():
    """Test image to ASCII conversion."""
    print("\nTesting Image to ASCII conversion...")
    
    # First create a simple test image
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple test image
        img = Image.new('RGB', (200, 100), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw some shapes
        draw.rectangle([20, 20, 80, 60], fill='black')
        draw.ellipse([100, 20, 160, 60], fill='gray')
        
        img.save("test_input.png")
        print("✓ Test image created")
        
        # Now convert to ASCII
        from asciivision import AsciiVision
        app = AsciiVision()
        
        ascii_result = app.image_to_ascii("test_input.png", width=50)
        
        if ascii_result:
            print("✓ Image to ASCII conversion successful!")
            print("Sample output:")
            print(ascii_result[:200] + "..." if len(ascii_result) > 200 else ascii_result)
            return True
        else:
            print("✗ Image to ASCII conversion failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error during Image to ASCII test: {e}")
        return False

def test_screen_reader_detection():
    """Test screen reader detection."""
    print("\nTesting Screen Reader Detection...")
    
    try:
        from asciivision import AsciiVision
        app = AsciiVision()
        
        screen_reader = app._detect_screen_reader()
        if screen_reader:
            print(f"✓ Screen reader detected: {screen_reader}")
        else:
            print("✓ No screen reader detected (expected in test environment)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during screen reader detection test: {e}")
        return False

def test_config_management():
    """Test configuration management."""
    print("\nTesting Configuration Management...")
    
    try:
        from asciivision import AsciiVision
        app = AsciiVision()
        
        # Test config loading
        config = app.config
        print(f"✓ Config loaded: {config}")
        
        # Test config saving
        original_auto_describe = config.get("auto_describe", False)
        config["auto_describe"] = True
        app._save_config()
        
        # Reload and verify
        app2 = AsciiVision()
        if app2.config.get("auto_describe") == True:
            print("✓ Config save/load successful!")
            
            # Restore original setting
            app2.config["auto_describe"] = original_auto_describe
            app2._save_config()
            return True
        else:
            print("✗ Config save/load failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error during config management test: {e}")
        return False

def cleanup():
    """Clean up test files."""
    test_files = ["test_output.png", "test_input.png"]
    for file in test_files:
        if Path(file).exists():
            Path(file).unlink()
            print(f"✓ Cleaned up {file}")

def main():
    """Run all tests."""
    print("AsciiVision Test Suite")
    print("=====================")
    
    tests = [
        test_ascii_to_image,
        test_image_to_ascii,
        test_screen_reader_detection,
        test_config_management
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    cleanup()

if __name__ == "__main__":
    main()
