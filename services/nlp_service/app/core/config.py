from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse NLP Service"

    DATABASE_URL: str = "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9093"
    KAFKA_DATA_COLLECTED_TOPIC: str = "company.data_collected"
    KAFKA_CONSUMER_GROUP_ID: str = "nlp-service"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()