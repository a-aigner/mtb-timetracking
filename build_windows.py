"""
Build script for Windows executable using PyInstaller.
"""
import PyInstaller.__main__
import sys
from pathlib import Path

def build_windows():
    """Build Windows executable."""
    
    # Get the project root directory
    root_dir = Path(__file__).parent
    
    PyInstaller.__main__.run([
        'main.py',
        '--name=MTBTimeTracker',
        '--windowed',  # No console window
        '--onefile',  # Create a directory with all dependencies
        '--icon=./logo.ico',  # Add icon file path if you have one
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

if __name__ == '__main__':
    build_windows()

