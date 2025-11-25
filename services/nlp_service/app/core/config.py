from shared.core.config import BaseAppSettings
from shared.core.events import TOPIC_DATA_COLLECTED, TOPIC_SIGNALS_READY


class Settings(BaseAppSettings):
    SERVICE_NAME: str = "nlp_service"

    PROJECT_NAME: str = "RiskPulse NLP Service"

    KAFKA_DATA_COLLECTED_TOPIC: str = TOPIC_DATA_COLLECTED
    KAFKA_SIGNALS_READY_TOPIC: str = TOPIC_SIGNALS_READY
    KAFKA_CONSUMER_GROUP_ID: str = "nlp-service"


settings = Settings()
