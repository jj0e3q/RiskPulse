from typing import Any, Dict
import logging

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def create_company(
    user_id: str,
    payload: Dict[str, Any],
) -> httpx.Response:
    url = str(settings.COMPANY_SERVICE_URL).rstrip('/')
    full_url = f"{url}/companies/"
    logger.info(f"Calling company service at {full_url} with payload: {payload}, user_id: {user_id}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.post(
                "/companies/",
                json=payload,
                headers={"X-User-Id": user_id},
            )
            logger.info(f"Company service responded with status {resp.status_code}")
            return resp
        except Exception as e:
            logger.error(f"Error calling company service at {full_url}: {e}", exc_info=True)
            raise


async def get_company_by_bin(
    user_id: str,
    bin_value: str,
) -> httpx.Response:
    url = str(settings.COMPANY_SERVICE_URL).rstrip('/')
    full_url = f"{url}/companies/by-bin/{bin_value}"
    logger.info(f"Calling company service at {full_url}, user_id: {user_id}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.get(
                f"/companies/by-bin/{bin_value}",
                headers={"X-User-Id": user_id},
            )
            logger.info(f"Company service responded with status {resp.status_code}")
            return resp
        except Exception as e:
            logger.error(f"Error calling company service at {full_url}: {e}", exc_info=True)
            raise

async def request_company_score(
    user_id: str,
    payload: Dict[str, Any],
) -> httpx.Response:
    url = str(settings.COMPANY_SERVICE_URL).rstrip('/')
    full_url = f"{url}/companies/score-request"
    logger.info(f"Calling company service at {full_url} with payload: {payload}, user_id: {user_id}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.post(
                "/companies/score-request",
                json=payload,
                headers={"X-User-Id": user_id},
            )
            logger.info(f"Company service responded with status {resp.status_code}")
            return resp
        except Exception as e:
            logger.error(f"Error calling company service at {full_url}: {e}", exc_info=True)
            raise