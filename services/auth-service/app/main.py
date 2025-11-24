from fastapi import FastAPI

from app.api.routes import auth as auth_routes
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}


app.include_router(auth_routes.router)