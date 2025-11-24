from sqlalchemy.orm import Session

from app.models.raw_event import RawEvent


def save_raw_event(
    db: Session,
    *,
    company_id: str | None,
    source: str,
    payload: dict,
) -> RawEvent:
    event = RawEvent(
        company_id=company_id,
        source=source,
        payload=payload,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
