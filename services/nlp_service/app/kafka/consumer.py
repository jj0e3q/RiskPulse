import json
from kafka import KafkaConsumer

from app.core.config import settings


def create_consumer() -> KafkaConsumer:
    consumer = KafkaConsumer(
        settings.KAFKA_DATA_COLLECTED_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP_ID,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=True,
        auto_offset_reset="earliest",
    )
    return consumer
