"""
Validation utilities for participant IDs and data.
"""
from typing import Optional, Tuple, List
from ..core.category import Category


def validate_participant_id(participant_id: str) -> Tuple[bool, str]:
    """
    Validate a participant ID format.
    
    Args:
        participant_id: The ID to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not participant_id:
        return False, "ID cannot be empty"
    
    # Remove whitespace
    participant_id = participant_id.strip()
    
    if not participant_id:
        return False, "ID cannot be empty"
    
    # Check if it's a valid format (allowing alphanumeric)
    if not participant_id.replace('-', '').replace('_', '').isalnum():
        return False, "ID can only contain letters, numbers, hyphens, and underscores"
    
    return True, ""


def find_participant_category(participant_id: str, categories: List[Category]) -> Optional[Category]:
    """
    Find which category a participant ID belongs to.
    
    Args:
        participant_id: The participant ID to search for
        categories: List of categories to search in
        
    Returns:
        The category containing the participant, or None if not found
    """
    participant_id = participant_id.strip()
    
    for category in categories:
        if category.has_participant(participant_id):
            return category
    
    return None


def get_participant_info(participant_id: str, category: Category) -> Optional[dict]:
    """
    Get participant information from a category.
    
    Args:
        participant_id: The participant ID
        category: The category to search in
        
    Returns:
        Participant data dictionary or None
    """
    return category.get_participant_data(participant_id)

