from kafka import KafkaConsumer

from app.core.config import settings
from shared.core.kafka import create_consumer as create_kafka_consumer


def create_consumer() -> KafkaConsumer:
    return create_kafka_consumer(
        settings,
        topic=settings.KAFKA_DATA_COLLECTED_TOPIC,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID,
    )
