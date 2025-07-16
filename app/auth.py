from fastapi import HTTPException, status, Header
from typing import Optional
from app.config import Config

async def verify_admin(admin_api_key: Optional[str] = Header(None)):
    if not admin_api_key or admin_api_key != Config.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key"
        )
    return True 