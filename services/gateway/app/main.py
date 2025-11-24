from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.clients import auth as auth_client


app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok", "service": "gateway"}


@app.post("/auth/register", tags=["auth"])
async def gateway_register(request: Request):
    payload = await request.json()
    resp = await auth_client.auth_register(payload)

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
    payload = await request.json()
    resp = await auth_client.auth_login(payload)

    try:
        content = resp.json() if resp.content else {}
    except Exception:
        content = {"detail": resp.text} if resp.text else {"detail": "Unknown error"}

    return JSONResponse(
        status_code=resp.status_code,
        content=content,
    )