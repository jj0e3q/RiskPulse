from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse API Gateway"

    SCORING_SERVICE_URL: AnyHttpUrl = "http://scoring_service:8000"
    AUTH_SERVICE_URL: AnyHttpUrl = "http://auth_service:8000"
    COMPANY_SERVICE_URL: AnyHttpUrl = "http://company_service:8000"

    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PROD"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()