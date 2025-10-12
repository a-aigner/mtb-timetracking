"""
Session management for saving and loading application state.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .category import Category
from ..utils.paths import get_sessions_dir, get_backups_dir, get_safe_filename


class Session:
    """Manages application session state and persistence."""
    
    def __init__(self):
        self.categories: List[Category] = []
        self.session_name: str = ""
        self.created_at: datetime = datetime.now()
        self.last_saved: Optional[datetime] = None
    
    def add_category(self, category: Category) -> None:
        """Add a category to the session."""
        self.categories.append(category)
    
    def remove_category(self, category_name: str) -> None:
        """Remove a category from the session."""
        self.categories = [c for c in self.categories if c.name != category_name]
    
    def get_category(self, category_name: str) -> Optional[Category]:
        """Get a category by name."""
        for category in self.categories:
            if category.name == category_name:
                return category
        return None
    
    def find_participant_category(self, participant_id: str) -> Optional[Category]:
        """Find which category a participant ID belongs to."""
        for category in self.categories:
            if category.has_participant(participant_id):
                return category
        return None
    
    def get_all_entries(self):
        """Get all entries from all categories."""
        all_entries = []
        for category in self.categories:
            all_entries.extend(category.entries)
        return sorted(all_entries, key=lambda e: e.finish_time, reverse=True)
    
    def save(self, filepath: Optional[Path] = None) -> Path:
        """
        Save session to JSON file.
        
        Args:
            filepath: Optional custom filepath. If None, uses default location.
            
        Returns:
            Path where the session was saved
        """
        if filepath is None:
            # Generate default filename
            if not self.session_name:
                self.session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            safe_name = get_safe_filename(self.session_name)
            filepath = get_sessions_dir() / f"{safe_name}.json"
        
        # Create backup if file already exists
        if filepath.exists():
            backup_dir = get_backups_dir()
            backup_name = f"{filepath.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_path = backup_dir / backup_name
            filepath.rename(backup_path)
        
        # Prepare data for serialization
        data = {
            'session_name': self.session_name,
            'created_at': self.created_at.isoformat(),
            'last_saved': datetime.now().isoformat(),
            'categories': [cat.to_dict() for cat in self.categories]
        }
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.last_saved = datetime.now()
        return filepath
    
    @classmethod
    def load(cls, filepath: Path) -> 'Session':
        """
        Load session from JSON file.
        
        Args:
            filepath: Path to the session file
            
        Returns:
            Loaded Session instance
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        session = cls()
        session.session_name = data['session_name']
        session.created_at = datetime.fromisoformat(data['created_at'])
        session.last_saved = datetime.fromisoformat(data['last_saved']) if data.get('last_saved') else None
        session.categories = [Category.from_dict(cat_data) for cat_data in data['categories']]
        
        return session
    
    @classmethod
    def get_latest_session(cls) -> Optional[Path]:
        """Get the path to the most recent session file."""
        sessions_dir = get_sessions_dir()
        session_files = list(sessions_dir.glob('*.json'))
        
        if not session_files:
            return None
        
        # Return the most recently modified file
        return max(session_files, key=lambda p: p.stat().st_mtime)
    
    def clear(self) -> None:
        """Clear all session data."""
        self.categories = []
        self.session_name = ""
        self.created_at = datetime.now()
        self.last_saved = None

