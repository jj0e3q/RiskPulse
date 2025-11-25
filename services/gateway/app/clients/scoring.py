import logging
from typing import Any, Dict

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def get_company_score(company_id: str) -> httpx.Response:
    url = str(settings.SCORING_SERVICE_URL).rstrip("/")
    full_url = f"{url}/scores/{company_id}"
    logger.info(f"Calling scoring service at {full_url}, company_id: {company_id}")
    async with httpx.AsyncClient(base_url=url, timeout=10.0) as client:
        try:
            resp = await client.get(f"/scores/{company_id}")
            logger.info(f"Scoring service responded with status {resp.status_code}")
            return resp
        except httpx.ConnectError as e:
            logger.error(
                f"Failed to connect to scoring service at {full_url}: {e}",
                exc_info=True,
            )
            raise
        except httpx.TimeoutException as e:
            logger.error(
                f"Timeout connecting to scoring service at {full_url}: {e}",
                exc_info=True,
            )
            raise
        except Exception as e:
            logger.error(
                f"Error calling scoring service at {full_url}: {e}", exc_info=True
            )
            raise
