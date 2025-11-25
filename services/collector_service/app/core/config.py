from shared.core.config import BaseAppSettings
from shared.core.events import TOPIC_SCORE_REQUESTED, TOPIC_DATA_COLLECTED


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "collector_service"

    PROJECT_NAME: str = "RiskPulse Collector Service"

    KAFKA_SCORE_REQUEST_TOPIC: str = TOPIC_SCORE_REQUESTED
    KAFKA_DATA_COLLECTED_TOPIC: str = TOPIC_DATA_COLLECTED
    KAFKA_CONSUMER_GROUP_ID: str = "collector-service"


settings = Settings()
