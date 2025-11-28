from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.security import verify_api_key

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency for authenticated endpoints
    """
    try:
        api_key = verify_api_key(credentials)
        return {"api_key": api_key}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # Changed from 401 to 403
            detail="Could not validate credentials"
        )