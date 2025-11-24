from typing import Any, Dict

import httpx

from app.core.config import settings


async def auth_register(payload: Dict[str, Any]) -> httpx.Response:
    async with httpx.AsyncClient(base_url=str(settings.AUTH_SERVICE_URL), timeout=10.0) as client:
        resp = await client.post("/auth/register", json=payload)
        return resp


async def auth_login(payload: Dict[str, Any]) -> httpx.Response:
    async with httpx.AsyncClient(base_url=str(settings.AUTH_SERVICE_URL), timeout=10.0) as client:
        resp = await client.post("/auth/login", json=payload)
        return resp