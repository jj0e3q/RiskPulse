import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def auth_register(payload: Dict[str, Any]) -> httpx.Response:
    url = str(settings.AUTH_SERVICE_URL).rstrip("/")
    full_url = f"{url}/auth/register"
    logger.info(f"Calling auth service at {full_url} with payload: {payload}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.post("/auth/register", json=payload)
            logger.info(f"Auth service responded with status {resp.status_code}")
            return resp
        except Exception as e:
            logger.error(
                f"Error calling auth service at {full_url}: {e}", exc_info=True
            )
            raise


async def auth_login(payload: Dict[str, Any]) -> httpx.Response:
    url = str(settings.AUTH_SERVICE_URL).rstrip("/")
    full_url = f"{url}/auth/login"
    logger.info(f"Calling auth service at {full_url} with payload: {payload}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.post("/auth/login", json=payload)
            logger.info(f"Auth service responded with status {resp.status_code}")
            return resp
        except Exception as e:
            logger.error(
                f"Error calling auth service at {full_url}: {e}", exc_info=True
            )
            raise
