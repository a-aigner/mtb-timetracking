"""
Build script for Linux executable using PyInstaller.
"""
import PyInstaller.__main__
import sys
from pathlib import Path

def build_linux():
    """Build Linux executable."""
    
    # Get the project root directory
    root_dir = Path(__file__).parent
    
    PyInstaller.__main__.run([
        'main.py',
        '--name=MTBTimeTracker',
        '--onedir',  # Create a directory with all dependencies
        '--icon=NONE',  # Add icon file path if you have one
        f'--distpath={root_dir / "dist"}',
        f'--workpath={root_dir / "build"}',
        f'--specpath={root_dir}',
        '--clean',
        '--noconfirm',
        # Hidden imports that might be needed
        '--hidden-import=openpyxl',
        '--hidden-import=pandas',
        '--hidden-import=PyQt6',
    ])
    
    print("\n" + "="*60)
    print("Build complete!")
    print(f"Executable location: {root_dir / 'dist' / 'MTBTimeTracker'}")
    print("="*60)
    print("\nTo run: ./dist/MTBTimeTracker/MTBTimeTracker")
    print("\nTo distribute:")
    print("1. Create a tarball: tar -czf MTBTimeTracker-linux.tar.gz dist/MTBTimeTracker")
    print("2. Or create a .deb package using 'fpm' or similar tools")
    print("3. Include README.md with the distribution")

if __name__ == '__main__':
    build_linux()

