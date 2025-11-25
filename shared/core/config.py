from typing import Literal

from pydantic_settings import BaseSettings


class BaseAppSettings(BaseSettings):
    """Base settings for all RiskPulse services."""

    DATABASE_URL: str = (
        "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"
    )

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9093"

    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PROD"
    JWT_ALGORITHM: str = "HS256"

    ENV: Literal["development", "staging", "production"] = "development"
    SERVICE_NAME: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True
