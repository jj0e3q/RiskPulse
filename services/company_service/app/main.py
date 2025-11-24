from fastapi import FastAPI

from app.core.config import settings
from app.api.routes import companies as companies_routes


app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "company_service"}


app.include_router(companies_routes.router)
