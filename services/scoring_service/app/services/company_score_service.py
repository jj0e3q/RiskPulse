from sqlalchemy.orm import Session
from sqlalchemy import select, desc

from app.models.company_score import CompanyScore
from app.models.normalized_event import NormalizedEvent
from app.services.scoring import compute_score


def calculate_and_save_score(db: Session, company_id: str) -> CompanyScore:
    stmt = select(NormalizedEvent).where(NormalizedEvent.company_id == company_id)
    events = db.execute(stmt).scalars().all()

    total_score, risk_level, details = compute_score(events)

    score = CompanyScore(
        company_id=company_id,
        total_score=total_score,
        risk_level=risk_level,
        details=details,
    )
    db.add(score)
    db.commit()
    db.refresh(score)
    return score


def get_latest_score(db: Session, company_id: str) -> CompanyScore | None:
    stmt = (
        select(CompanyScore)
        .where(CompanyScore.company_id == company_id)
        .order_by(desc(CompanyScore.calculated_at))
    )
    return db.execute(stmt).scalars().first()
