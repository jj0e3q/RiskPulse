from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead
from app.kafka.producer import send_score_requested_event


router = APIRouter(prefix="/companies", tags=["companies"])


class ScoreRequestPayload(CompanyCreate):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(get_db),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """
    Создаёт компанию. X-User-Id пока просто принимаем для будущего аудита/мультиарендности.
    """
    existing = db.query(Company).filter(Company.bin == company_in.bin).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this BIN already exists",
        )

    company = Company(
        bin=company_in.bin,
        name=company_in.name,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("/by-bin/{bin}", response_model=CompanyRead)
def get_company_by_bin(
    bin: str,
    db: Session = Depends(get_db),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    company = db.query(Company).filter(Company.bin == bin).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.get("/{company_id}", response_model=CompanyRead)
def get_company_by_id(
    company_id: str,
    db: Session = Depends(get_db),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )
    return company


@router.post("/score-request")
def request_company_score(
    payload: ScoreRequestPayload,
    db: Session = Depends(get_db),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
):
    """
    1) Находит или создаёт компанию по BIN.
    2) Шлёт событие company.score_requested в Kafka.
    """

    company = db.query(Company).filter(Company.bin == payload.bin).first()
    if not company:
        company = Company(
            bin=payload.bin,
            name=payload.name,
        )
        db.add(company)
        db.commit()
        db.refresh(company)

    send_score_requested_event(
        company_id=company.id,
        bin_value=company.bin,
        requested_by=x_user_id,
    )

    return {
        "status": "score_requested",
        "company_id": company.id,
        "bin": company.bin,
    }
