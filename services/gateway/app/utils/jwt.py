from typing import Any

from fastapi import HTTPException, status

from app.core.config import settings
from shared.core.jwt import decode_access_token


def decode_jwt_token(token: str) -> dict[str, Any]:
    try:
        return decode_access_token(settings, token)
    except ValueError as e:
        error_msg = str(e)
        if "expired" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
