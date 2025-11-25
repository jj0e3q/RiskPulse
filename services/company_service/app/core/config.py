from shared.core.config import BaseAppSettings
from shared.core.events import TOPIC_SCORE_REQUESTED


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "company_service"

    PROJECT_NAME: str = "RiskPulse"

    KAFKA_SCORE_REQUEST_TOPIC: str = TOPIC_SCORE_REQUESTED


settings = Settings()