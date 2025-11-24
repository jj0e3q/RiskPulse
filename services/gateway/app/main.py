from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import httpx
import logging

from app.core.config import settings
from app.clients import auth as auth_client
from app.clients import company as company_client
from app.api.deps import get_current_user_id

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "gateway"}


@app.post("/auth/register", tags=["auth"])
async def gateway_register(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse request JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in request body"
        )
    
    try:
        resp = await auth_client.auth_register(payload)
    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service is unavailable"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Auth service request timeout"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling auth service: {str(e)}"
        )

    # прокидываем статус и тело как есть
    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )


@app.post("/auth/login", tags=["auth"])
async def gateway_login(request: Request):
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse request JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in request body"
        )
    
    try:
        resp = await auth_client.auth_login(payload)
    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Auth service is unavailable"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Auth service request timeout"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling auth service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling auth service: {str(e)}"
        )

    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )

@app.get("/me", tags=["auth"])
async def get_me(
    user_id: str = Depends(get_current_user_id),
):
    return {"user_id": user_id}

@app.post("/companies", tags=["companies"])
async def gateway_create_company(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse request JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in request body"
        )
    
    try:
        resp = await company_client.create_company(user_id=user_id, payload=payload)
    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Company service is unavailable"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Company service request timeout"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling company service: {str(e)}"
        )

    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )


@app.get("/companies/by-bin/{bin_value}", tags=["companies"])
async def gateway_get_company_by_bin(
    bin_value: str,
    user_id: str = Depends(get_current_user_id),
):
    try:
        resp = await company_client.get_company_by_bin(user_id=user_id, bin_value=bin_value)
    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Company service is unavailable"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Company service request timeout"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling company service: {str(e)}"
        )

    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )

@app.post("/score/request", tags=["score"])
async def gateway_request_score(
    request: Request,
    user_id: str = Depends(get_current_user_id),
):
    """
    Внешняя ручка:
    - принимает BIN (и опционально name),
    - валидирует JWT,
    - прокидывает X-User-Id в company_service,
    - тот кидает событие в Kafka.
    """
    try:
        payload = await request.json()
    except Exception as e:
        logger.error(f"Failed to parse request JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON in request body"
        )
    
    try:
        resp = await company_client.request_company_score(
            user_id=user_id,
            payload=payload,
        )
    except httpx.ConnectError as e:
        logger.error(f"Failed to connect to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Company service is unavailable"
        )
    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Company service request timeout"
        )
    except Exception as e:
        logger.error(f"Unexpected error calling company service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calling company service: {str(e)}"
        )

    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )