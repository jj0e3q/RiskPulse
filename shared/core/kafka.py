import json

from kafka import KafkaConsumer, KafkaProducer

from shared.core.config import BaseAppSettings

# Cache producers by bootstrap_servers
_producer_cache: dict[str, KafkaProducer] = {}


def get_producer(settings: BaseAppSettings) -> KafkaProducer:
    bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
    if bootstrap_servers not in _producer_cache:
        _producer_cache[bootstrap_servers] = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return _producer_cache[bootstrap_servers]


def create_consumer(
    settings: BaseAppSettings,
    topic: str,
    group_id: str,
    auto_offset_reset: str = "earliest",
    enable_auto_commit: bool = True,
) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        enable_auto_commit=enable_auto_commit,
        auto_offset_reset=auto_offset_reset,
    )
