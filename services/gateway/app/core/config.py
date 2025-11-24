from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse API Gateway"

    AUTH_SERVICE_URL: AnyHttpUrl = "http://auth_service:8000"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()