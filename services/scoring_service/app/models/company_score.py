from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CompanyScore(Base):
    __tablename__ = "company_scores"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    company_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)

    total_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)

    details: Mapped[dict] = mapped_column(JSONB, nullable=False)

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )
