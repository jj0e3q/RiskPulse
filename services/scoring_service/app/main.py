import logging
import threading
import time
from typing import Generator

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.kafka.consumer import create_consumer
from app.schemas.company_score import CompanyScoreRead
from app.services.company_score_service import (
    calculate_and_save_score,
    get_latest_score,
)
from shared.core.logging import setup_logging

setup_logging(settings.SERVICE_NAME)

app = FastAPI(title=settings.PROJECT_NAME)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def consumer_loop():
    while True:
        try:
            consumer = create_consumer()
            db = SessionLocal()
            try:
                for msg in consumer:
                    event = msg.value
                    company_id = event.get("company_id")
                    bin_value = event.get("bin")
                    logging.info(
                        "Received signals_ready event: company_id=%s bin=%s",
                        company_id,
                        bin_value,
                    )
                    try:
                        calculate_and_save_score(db, company_id)
                        logging.info("Score calculated and saved for company_id=%s", company_id)
                    except Exception as e:
                        logging.error("Error calculating score: %s", e)
            finally:
                db.close()
        except Exception as e:
            logging.error("Error in scoring consumer loop: %s", e)
            time.sleep(5)


@app.on_event("startup")
def start_consumer():
    t = threading.Thread(target=consumer_loop, daemon=True)
    t.start()


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "scoring_service"}


@app.get("/scores/{company_id}", response_model=CompanyScoreRead, tags=["scores"])
def get_company_score(company_id: str, db: Session = Depends(get_db)):
    try:
        score = get_latest_score(db, company_id)
        if not score:
            raise HTTPException(status_code=404, detail="Score not found for this company")
        return score
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error getting score for company_id={company_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")