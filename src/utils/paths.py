"""
Cross-platform path management utilities.
Ensures proper path handling across Windows, macOS, and Linux.
"""
import os
from pathlib import Path
from typing import Union


def get_app_data_dir() -> Path:
    """
    Get the application data directory based on the operating system.
    
    Returns:
        Path object for the app data directory
    """
    if os.name == 'nt':  # Windows
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    elif os.name == 'posix':
        if 'darwin' in os.uname().sysname.lower():  # macOS
            base = Path.home() / 'Library' / 'Application Support'
        else:  # Linux
            base = Path(os.environ.get('XDG_DATA_HOME', Path.home() / '.local' / 'share'))
    else:
        base = Path.home()
    
    app_dir = base / 'MTBTimeTracker'
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir


def get_sessions_dir() -> Path:
    """
    Get the sessions directory for storing session data.
    
    Returns:
        Path object for the sessions directory
    """
    sessions_dir = get_app_data_dir() / 'sessions'
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir


def get_backups_dir() -> Path:
    """
    Get the backups directory for storing backup data.
    
    Returns:
        Path object for the backups directory
    """
    backups_dir = get_app_data_dir() / 'backups'
    backups_dir.mkdir(parents=True, exist_ok=True)
    return backups_dir


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Normalize a path to use forward slashes and resolve it.
    
    Args:
        path: Path to normalize
        
    Returns:
        Normalized Path object
    """
    return Path(path).resolve()


def get_safe_filename(filename: str) -> str:
    """
    Convert a filename to a safe version that works on all platforms.
    Removes or replaces characters that are problematic on Windows, macOS, or Linux.
    
    Args:
        filename: Original filename
        
    Returns:
        Safe filename string
    """
    # Characters that are invalid on Windows
    invalid_chars = '<>:"/\\|?*'
    
    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    safe_name = safe_name.strip('. ')
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = 'unnamed'
    
    return safe_name

