"""
Build script for macOS application bundle using PyInstaller.
"""
import PyInstaller.__main__
import sys
from pathlib import Path

def build_macos():
    """Build macOS application bundle."""
    
    # Get the project root directory
    root_dir = Path(__file__).parent
    
    PyInstaller.__main__.run([
        'main.py',
        '--name=MTBTimeTracker',
        '--windowed',  # Create .app bundle
        '--onedir',  # Create a directory with all dependencies
        '--icon=NONE',  # Add .icns file path if you have one
        f'--distpath={root_dir / "dist"}',
        f'--workpath={root_dir / "build"}',
        f'--specpath={root_dir}',
        '--clean',
        '--noconfirm',
        # macOS specific options
        '--osx-bundle-identifier=com.mtbtimetracker.app',
        # Hidden imports that might be needed
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=PyQt6',
    ])
    
    print("\n" + "="*60)
    print("Build complete!")
    print(f"Application location: {root_dir / 'dist' / 'MTBTimeTracker.app'}")
    print("="*60)
    print("\nTo distribute:")
    print("1. Test the app by double-clicking MTBTimeTracker.app")
    print("2. Create a .dmg: Use 'hdiutil' or a tool like 'create-dmg'")
    print("3. For code signing: Use 'codesign' with your Apple Developer certificate")

if __name__ == '__main__':
    build_macos()

