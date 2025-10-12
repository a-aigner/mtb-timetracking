"""
Excel export utilities for generating result files.
"""
import pandas as pd
from pathlib import Path
from typing import List
from datetime import datetime
from ..core.category import Category
from ..core.entry import FinishEntry
from .paths import get_safe_filename


def export_to_excel(categories: List[Category], filepath: Path) -> None:
    """
    Export race results to an Excel file with multiple sheets.
    
    Args:
        categories: List of categories with their results
        filepath: Path where to save the Excel file
    """
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Create a sheet for each category
        for category in categories:
            if category.entries:
                df = _create_category_dataframe(category)
                # Sheet names have a 31 character limit in Excel
                sheet_name = category.name[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Create combined sheet with all results
        if any(cat.entries for cat in categories):
            combined_df = _create_combined_dataframe(categories)
            combined_df.to_excel(writer, sheet_name='All Results', index=False)
        
        # Create sheet for invalid IDs
        invalid_df = _create_invalid_ids_dataframe(categories)
        if not invalid_df.empty:
            invalid_df.to_excel(writer, sheet_name='Invalid IDs', index=False)


def _create_category_dataframe(category: Category) -> pd.DataFrame:
    """
    Create a DataFrame for a single category's results.
    
    Args:
        category: The category to export
        
    Returns:
        DataFrame with category results
    """
    # Get sorted entries
    sorted_entries = category.get_sorted_entries()
    
    # Prepare data rows
    rows = []
    for rank, entry in enumerate(sorted_entries, start=1):
        if entry.is_dnf:
            continue  # Skip DNF entries in ranking
        
        row = {
            'Rank': rank,
            'ID': entry.participant_id,
            'First Name': entry.first_name or '',
            'Last Name': entry.last_name or '',
            'Team': entry.team or '',
            'Birth Year': entry.birth_year or '',
            'Gender': entry.gender or '',
            'Finish Time': entry.format_finish_time(),
            'Elapsed Time': entry.format_elapsed_time(),
            'Notes': entry.notes or ''
        }
        rows.append(row)
    
    # Add DNF entries at the end
    for entry in sorted_entries:
        if entry.is_dnf:
            row = {
                'Rank': 'DNF',
                'ID': entry.participant_id,
                'First Name': entry.first_name or '',
                'Last Name': entry.last_name or '',
                'Team': entry.team or '',
                'Birth Year': entry.birth_year or '',
                'Gender': entry.gender or '',
                'Finish Time': entry.format_finish_time(),
                'Elapsed Time': entry.format_elapsed_time(),
                'Notes': entry.notes or ''
            }
            rows.append(row)
    
    return pd.DataFrame(rows)


def _create_combined_dataframe(categories: List[Category]) -> pd.DataFrame:
    """
    Create a combined DataFrame with all categories' results.
    
    Args:
        categories: List of all categories
        
    Returns:
        Combined DataFrame with all results
    """
    rows = []
    
    for category in categories:
        for entry in category.entries:
            if entry.is_dnf:
                rank = 'DNF'
            else:
                # Calculate rank within category
                sorted_entries = [e for e in category.get_sorted_entries() if not e.is_dnf]
                rank = sorted_entries.index(entry) + 1 if entry in sorted_entries else 'DNF'
            
            row = {
                'Category': category.name,
                'Rank': rank,
                'ID': entry.participant_id,
                'First Name': entry.first_name or '',
                'Last Name': entry.last_name or '',
                'Team': entry.team or '',
                'Birth Year': entry.birth_year or '',
                'Gender': entry.gender or '',
                'Finish Time': entry.format_finish_time(),
                'Elapsed Time': entry.format_elapsed_time(),
                'Notes': entry.notes or ''
            }
            rows.append(row)
    
    # Sort by elapsed time
    df = pd.DataFrame(rows)
    if not df.empty:
        # Convert elapsed time to seconds for sorting
        df['_sort_key'] = df['Elapsed Time'].apply(_parse_time_to_seconds)
        df = df.sort_values('_sort_key')
        df = df.drop('_sort_key', axis=1)
    
    return df


def _create_invalid_ids_dataframe(categories: List[Category]) -> pd.DataFrame:
    """
    Create a DataFrame with all entries that have invalid IDs.
    
    Args:
        categories: List of all categories
        
    Returns:
        DataFrame with invalid ID entries
    """
    rows = []
    
    for category in categories:
        for entry in category.entries:
            if not entry.is_valid_id:
                row = {
                    'Category': category.name,
                    'ID': entry.participant_id,
                    'First Name': entry.first_name or 'Unknown',
                    'Last Name': entry.last_name or 'Unknown',
                    'Team': entry.team or '',
                    'Birth Year': entry.birth_year or '',
                    'Gender': entry.gender or '',
                    'Finish Time': entry.format_finish_time(),
                    'Elapsed Time': entry.format_elapsed_time(),
                    'Notes': entry.notes or 'ID not found in category CSV'
                }
                rows.append(row)
    
    return pd.DataFrame(rows)


def _parse_time_to_seconds(time_str: str) -> float:
    """Parse HH:MM:SS format to total seconds."""
    try:
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    except:
        return float('inf')  # Put invalid times at the end


def generate_default_filename() -> str:
    """Generate a default filename for export with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return get_safe_filename(f"race_results_{timestamp}.xlsx")

