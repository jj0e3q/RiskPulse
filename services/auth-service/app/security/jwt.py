from datetime import timedelta
from typing import Any, Optional

from shared.core.jwt import (
    create_access_token as _create_access_token,
    decode_access_token as _decode_access_token,
)

from app.core.config import settings


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_access_token(settings, subject, expires_delta)


def decode_access_token(token: str) -> dict[str, Any]:
    return _decode_access_token(settings, token)
