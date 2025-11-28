import re
from datetime import datetime
from fastapi import HTTPException, status

def validate_polymer_string(polymer: str) -> bool:
    """
    Validate polymer string format.
    
    Args:
        polymer: Polymer string to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If polymer is invalid
    """
    if not polymer:
        raise ValueError("Polymer cannot be empty")
    
    if len(polymer) < 1 or len(polymer) > 128:
        raise ValueError("Polymer must be between 1 and 128 characters")
    
    if not re.match(r'^[a-zA-Z]+$', polymer):
        raise ValueError("Polymer must contain only letters (a-z, A-Z)")
    
    return True

def validate_timestamp(timestamp: datetime) -> bool:
    """
    Validate timestamp is reasonable (not in future, not too far in past).
    
    Args:
        timestamp: Timestamp to validate
        
    Returns:
        bool: True if valid
    """
    now = datetime.utcnow()
    
    # Allow some leeway for timezone differences
    if timestamp > now:
        raise ValueError("Timestamp cannot be in the future")
    
    # Reject timestamps too far in the past (10 years)
    if (now - timestamp).days > 3650:
        raise ValueError("Timestamp is too far in the past")
    
    return True

def validate_time_range(start: datetime, end: datetime) -> bool:
    """
    Validate that start time is before end time.
    
    Args:
        start: Start timestamp
        end: End timestamp
        
    Returns:
        bool: True if valid
    """
    if start >= end:
        raise ValueError("Start timestamp must be before end timestamp")
    
    # Prevent excessively large time ranges
    if (end - start).days > 365:
        raise ValueError("Time range cannot exceed 1 year")
    
    return True