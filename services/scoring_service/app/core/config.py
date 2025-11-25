from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse Scoring Service"

    DATABASE_URL: str = "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9093"
    KAFKA_SIGNALS_READY_TOPIC: str = "company.signals_ready"
    KAFKA_CONSUMER_GROUP_ID: str = "scoring-service"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()