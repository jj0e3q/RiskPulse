import json
from datetime import datetime, timezone

from kafka import KafkaProducer

from app.core.config import settings


producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return producer


def send_data_collected_event(
    *,
    company_id: str,
    bin_value: str,
    requested_by: str | None,
    collected_sources: list[str],
) -> None:
    event = {
        "event_type": "company.data_collected",
        "company_id": company_id,
        "bin": bin_value,
        "requested_by": requested_by,
        "collected_sources": collected_sources,
        "collected_at": datetime.now(timezone.utc).isoformat(),
    }
    prod = get_producer()
    prod.send(settings.KAFKA_DATA_COLLECTED_TOPIC, value=event)
