from shared.core.config import BaseAppSettings
from shared.core.events import TOPIC_SIGNALS_READY


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "scoring_service"

    PROJECT_NAME: str = "RiskPulse Scoring Service"

    KAFKA_SIGNALS_READY_TOPIC: str = TOPIC_SIGNALS_READY
    KAFKA_CONSUMER_GROUP_ID: str = "scoring-service"


settings = Settings()