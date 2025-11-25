import logging
import time

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.kafka.consumer import create_consumer
from app.kafka.producer import send_data_collected_event
from app.services.raw_event_service import save_raw_event
from shared.core.logging import setup_logging

setup_logging(settings.SERVICE_NAME)


def process_message(db: Session, event: dict) -> None:
    company_id = event.get("company_id")
    bin_value = event.get("bin")
    requested_by = event.get("requested_by")

    logging.info(
        "Processing score request event: company_id=%s bin=%s requested_by=%s",
        company_id,
        bin_value,
        requested_by,
    )

    save_raw_event(
        db,
        company_id=company_id,
        source="score_request",
        payload=event,
    )

    collected_sources = ["score_request"]

    send_data_collected_event(
        company_id=company_id,
        bin_value=bin_value,
        requested_by=requested_by,
        collected_sources=collected_sources,
    )


def run():
    logging.info("Starting Collector Service")
    logging.info(
        "Connecting to Kafka at %s, topic=%s",
        settings.KAFKA_BOOTSTRAP_SERVERS,
        settings.KAFKA_SCORE_REQUEST_TOPIC,
    )

    consumer = create_consumer()

    db = SessionLocal()
    try:
        for msg in consumer:
            event = msg.value
            try:
                process_message(db, event)
            except Exception as e:
                logging.error("Error processing message: %s", e)
    finally:
        db.close()


if __name__ == "__main__":
    for attempt in range(10):
        try:
            run()
        except Exception as e:
            logging.error("Error in collector: %s", e)
            time.sleep(5)
