"""
Finish entry model for tracking individual finish times.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class FinishEntry:
    """Represents a single finish line entry for a participant."""
    
    entry_id: str  # Unique identifier for this entry
    participant_id: str  # ID of the participant
    category_name: str  # Name of the category
    finish_time: datetime  # Absolute timestamp when they finished
    elapsed_time: timedelta  # Time since category start
    
    # Participant information (from CSV)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    team: Optional[str] = None
    birth_year: Optional[str] = None
    gender: Optional[str] = None
    
    # Metadata
    is_valid_id: bool = True  # False if ID wasn't found in any category
    is_dnf: bool = False  # Did Not Finish flag
    notes: str = ""
    
    def to_dict(self) -> dict:
        """Convert entry to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert datetime and timedelta to strings
        data['finish_time'] = self.finish_time.isoformat()
        data['elapsed_time'] = str(self.elapsed_time)
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FinishEntry':
        """Create entry from dictionary (for JSON deserialization)."""
        data = data.copy()
        data['finish_time'] = datetime.fromisoformat(data['finish_time'])
        
        # Parse elapsed_time from string format "H:MM:SS" or "H:MM:SS.microseconds"
        time_str = data['elapsed_time']
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        microseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
        
        data['elapsed_time'] = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        )
        
        return cls(**data)
    
    def get_full_name(self) -> str:
        """Get participant's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return f"ID: {self.participant_id}"
    
    def format_elapsed_time(self) -> str:
        """Format elapsed time as HH:MM:SS."""
        total_seconds = int(self.elapsed_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_finish_time(self) -> str:
        """Format finish time as HH:MM:SS."""
        return self.finish_time.strftime("%H:%M:%S")

