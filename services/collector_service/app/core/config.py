from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse Collector Service"

    DATABASE_URL: str = "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9093"
    KAFKA_SCORE_REQUEST_TOPIC: str = "company.score_requested"
    KAFKA_DATA_COLLECTED_TOPIC: str = "company.data_collected"
    KAFKA_CONSUMER_GROUP_ID: str = "collector-service"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
