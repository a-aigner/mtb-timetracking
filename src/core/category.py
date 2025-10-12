"""
Category data model for managing race categories.
"""
import pandas as pd
from typing import List, Optional, Dict
from pathlib import Path
from .timer import Timer
from .entry import FinishEntry


class Category:
    """Represents a race category with participants and timing."""
    
    def __init__(self, name: str, csv_path: Optional[Path] = None, 
                 id_column: str = 'ID', dataframe: Optional[pd.DataFrame] = None):
        self.name = name
        self.csv_path = csv_path
        self.id_column = id_column
        self.timer = Timer()
        self.entries: List[FinishEntry] = []
        
        # Store participant data
        self.participants: Dict[str, dict] = {}
        
        if dataframe is not None:
            self._load_from_dataframe(dataframe)
        elif csv_path:
            self._load_from_csv()
    
    def _load_from_csv(self) -> None:
        """Load participant data from CSV file."""
        try:
            # Try different delimiters and encodings - NO HEADER ROW
            df = None
            for delimiter in [';', ',', '\t']:
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        # Read CSV without header (header=None)
                        temp_df = pd.read_csv(self.csv_path, delimiter=delimiter, encoding=encoding, header=None)
                        if len(temp_df.columns) > 1:  # Valid CSV should have multiple columns
                            df = temp_df
                            break
                    except:
                        continue
                if df is not None:
                    break
            
            if df is None:
                raise ValueError(f"Could not parse CSV file: {self.csv_path}")
            
            # Create column names as A, B, C, D, etc.
            column_letters = []
            for i in range(len(df.columns)):
                if i < 26:
                    column_letters.append(chr(65 + i))  # A-Z
                else:
                    # For more than 26 columns: AA, AB, AC, etc.
                    first = chr(65 + (i // 26) - 1)
                    second = chr(65 + (i % 26))
                    column_letters.append(first + second)
            
            df.columns = column_letters
            
            # Clean data
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].astype(str).str.strip().str.strip('"')
            
            self._load_from_dataframe(df)
            
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
    
    def _load_from_dataframe(self, df: pd.DataFrame) -> None:
        """Load participant data from a pandas DataFrame."""
        # Clean all string data (remove quotes)
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.strip('"')
        
        # Store the dataframe
        self.dataframe = df
        
        # Build participant lookup dictionary
        if self.id_column not in df.columns:
            raise ValueError(f"ID column '{self.id_column}' not found in CSV")
        
        # Expected format (based on sample files):
        # Column A (0): ID
        # Column B (1): First Name
        # Column C (2): Last Name
        # Column D (3): Team
        # Column E (4): Birth Year
        # Column F (5): Gender
        
        for _, row in df.iterrows():
            participant_id = str(row[self.id_column]).strip()
            if participant_id and participant_id != 'nan':
                # Map columns by index for CSV files without headers
                cols = df.columns.tolist()
                self.participants[participant_id] = {
                    'id': participant_id,
                    'first_name': str(row[cols[1]]).strip() if len(cols) > 1 and str(row[cols[1]]) != 'nan' else '',
                    'last_name': str(row[cols[2]]).strip() if len(cols) > 2 and str(row[cols[2]]) != 'nan' else '',
                    'team': str(row[cols[3]]).strip() if len(cols) > 3 and str(row[cols[3]]) != 'nan' else '',
                    'birth_year': str(row[cols[4]]).strip() if len(cols) > 4 and str(row[cols[4]]) != 'nan' else '',
                    'gender': str(row[cols[5]]).strip() if len(cols) > 5 and str(row[cols[5]]) != 'nan' else ''
                }
    
    def get_participant_data(self, participant_id: str) -> Optional[dict]:
        """Get participant data by ID."""
        return self.participants.get(str(participant_id).strip())
    
    def has_participant(self, participant_id: str) -> bool:
        """Check if a participant ID exists in this category."""
        return str(participant_id).strip() in self.participants
    
    def add_entry(self, entry: FinishEntry) -> None:
        """Add a finish entry to this category."""
        self.entries.append(entry)
    
    def get_total_participants(self) -> int:
        """Get total number of participants in this category."""
        return len(self.participants)
    
    def get_finished_count(self) -> int:
        """Get number of participants who have finished."""
        return len([e for e in self.entries if not e.is_dnf])
    
    def get_recent_entries(self, count: int = 15) -> List[FinishEntry]:
        """Get the most recent finish entries."""
        return self.entries[-count:] if self.entries else []
    
    def get_sorted_entries(self) -> List[FinishEntry]:
        """Get all entries sorted by elapsed time."""
        return sorted(self.entries, key=lambda e: e.elapsed_time)
    
    def to_dict(self) -> dict:
        """Convert category to dictionary for serialization."""
        return {
            'name': self.name,
            'csv_path': str(self.csv_path) if self.csv_path else None,
            'id_column': self.id_column,
            'timer': self.timer.to_dict(),
            'entries': [entry.to_dict() for entry in self.entries],
            'participants': self.participants
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        """Create category from dictionary (for deserialization)."""
        csv_path = Path(data['csv_path']) if data['csv_path'] else None
        category = cls(data['name'], csv_path=csv_path, id_column=data['id_column'])
        category.timer = Timer.from_dict(data['timer'])
        category.entries = [FinishEntry.from_dict(e) for e in data['entries']]
        category.participants = data['participants']
        return category

