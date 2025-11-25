from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import companies as companies_routes
from shared.core.logging import setup_logging

setup_logging(settings.SERVICE_NAME)

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "company_service"}


app.include_router(companies_routes.router)
