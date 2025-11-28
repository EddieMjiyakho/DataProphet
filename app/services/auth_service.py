from fastapi import HTTPException, status
from app.core.config import settings

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided API key against configured keys.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    return api_key in settings.api_keys

def get_api_key_user(api_key: str) -> dict:
    """
    Get user information for a valid API key.
    In a real system, this would query a users table.
    
    Args:
        api_key: Valid API key
        
    Returns:
        dict: User information
    """
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # In a real application, you'd fetch user details from a database
    return {
        "api_key": api_key,
        "user_id": f"user_{api_key[-4:]}",  # Mock user ID
        "role": "user"
    }