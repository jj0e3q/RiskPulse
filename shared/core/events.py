from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field


# Topic name constants
TOPIC_SCORE_REQUESTED = "company.score_requested"
TOPIC_DATA_COLLECTED = "company.data_collected"
TOPIC_SIGNALS_READY = "company.signals_ready"


class CompanyScoreRequested(BaseModel):
    event_type: str = Field(default="company.score_requested", frozen=True)
    company_id: str
    bin: str
    requested_by: Optional[str] = None
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with ISO format datetime."""
        return {
            "event_type": self.event_type,
            "company_id": self.company_id,
            "bin": self.bin,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at.isoformat(),
        }


class CompanyDataCollected(BaseModel):
    event_type: str = Field(default="company.data_collected", frozen=True)
    company_id: str
    bin: Optional[str] = None
    requested_by: Optional[str] = None
    collected_sources: list[str]
    collected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with ISO format datetime."""
        return {
            "event_type": self.event_type,
            "company_id": self.company_id,
            "bin": self.bin,
            "requested_by": self.requested_by,
            "collected_sources": self.collected_sources,
            "collected_at": self.collected_at.isoformat(),
        }


class CompanySignalsReady(BaseModel):
    event_type: str = Field(default="company.signals_ready", frozen=True)
    company_id: str
    bin: Optional[str] = None
    signals_count: int
    ready_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with ISO format datetime."""
        return {
            "event_type": self.event_type,
            "company_id": self.company_id,
            "bin": self.bin,
            "signals_count": self.signals_count,
            "ready_at": self.ready_at.isoformat(),
        }

