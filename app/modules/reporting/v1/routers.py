from fastapi import APIRouter, Depends
from requests import Session
from .services import get_jobs_count
from .schemas import JobCountResponse
from app.core.database import get_db

router = APIRouter()


@router.get("/jobs", response_model=JobCountResponse)
def jobs_report(db: Session = Depends(get_db)):
    return get_jobs_count(db)


@router.get("/health")
def health():
    return {"status": "reporting service running"}