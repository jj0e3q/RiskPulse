from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "RiskPulse"

    DATABASE_URL: str = "postgresql+psycopg2://riskpulse:riskpulse@localhost:5432/riskpulse"

    JWT_SECRET_KEY: str = "CHANGE_ME_IN_PROD"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()