from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse"

    DATABASE_URL: str = "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9093"
    KAFKA_SCORE_REQUEST_TOPIC: str = "company.score_requested"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()