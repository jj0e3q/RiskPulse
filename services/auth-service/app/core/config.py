from shared.core.config import BaseAppSettings


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "auth_service"

    PROJECT_NAME: str = "RiskPulse"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()