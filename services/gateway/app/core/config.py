from pydantic import AnyHttpUrl

from shared.core.config import BaseAppSettings


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "gateway"

    PROJECT_NAME: str = "RiskPulse API Gateway"

    SCORING_SERVICE_URL: AnyHttpUrl = "http://scoring_service:8000"
    AUTH_SERVICE_URL: AnyHttpUrl = "http://auth_service:8000"
    COMPANY_SERVICE_URL: AnyHttpUrl = "http://company_service:8000"


settings = Settings()
