import logging
import time

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.kafka.consumer import create_consumer
from app.kafka.producer import send_signals_ready_event
from app.services.nlp_engine import classify_events
from app.services.normalized_event_service import save_normalized_events

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def fetch_raw_events_for_company(db: Session, company_id: str) -> list[dict]:
    from sqlalchemy import select
    from app.models.raw_event import RawEvent

    stmt = select(RawEvent).where(RawEvent.company_id == company_id)
    rows = db.execute(stmt).scalars().all()

    return [
        {
            "company_id": r.company_id,
            "source": r.source,
            "payload": r.payload,
        }
        for r in rows
    ]


def run():
    logging.info("Starting NLP Service")
    consumer = create_consumer()

    db = SessionLocal()
    try:
        for msg in consumer:
            event = msg.value
            company_id = event.get("company_id")
            bin_value = event.get("bin")

            logging.info(
                "Received data_collected event: company_id=%s bin=%s",
                company_id,
                bin_value,
            )

            try:
                raw_events = fetch_raw_events_for_company(db, company_id)
                if not raw_events:
                    logging.info("No raw events found for company_id=%s", company_id)
                    continue

                normalized = classify_events(raw_events)
                save_normalized_events(db, normalized)
                signals_count = len(normalized)
                logging.info(
                    "Saved %s normalized events for company_id=%s",
                    len(normalized),
                    company_id,
                )
                send_signals_ready_event(
                    company_id=company_id,
                    bin_value=bin_value,
                    signals_count=signals_count,
                )
            except Exception as e:
                logging.error("Error processing data_collected event: %s", e)

    finally:
        db.close()


if __name__ == "__main__":
    for attempt in range(10):
        try:
            run()
        except Exception as e:
            logging.error("Error in NLP service (attempt %s): %s", attempt + 1, e)
            time.sleep(5)
