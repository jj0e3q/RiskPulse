from datetime import datetime
from pydantic import BaseModel, Field


class CompanyBase(BaseModel):
    bin: str = Field(..., min_length=6, max_length=20)
    name: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyRead(CompanyBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
