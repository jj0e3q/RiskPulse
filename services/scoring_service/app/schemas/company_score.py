from datetime import datetime
from pydantic import BaseModel


class CompanyScoreRead(BaseModel):
    company_id: str
    total_score: int
    risk_level: str
    details: dict
    calculated_at: datetime

    class Config:
        from_attributes = True

