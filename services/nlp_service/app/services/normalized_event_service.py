from datetime import datetime
from uuid import uuid4
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.normalized_event import NormalizedEvent


def save_normalized_events(
    db: Session,
    events: List[Dict[str, Any]],
) -> None:
    for ev in events:
        obj = NormalizedEvent(
            id=str(uuid4()),
            company_id=ev["company_id"],
            event_type=ev["event_type"],
            severity=ev["severity"],
            description=ev["description"],
            source=ev["source"],
            event_date=ev.get("event_date"),
            meta=ev.get("meta"),
            created_at=datetime.utcnow(),
        )
        db.add(obj)
    db.commit()
