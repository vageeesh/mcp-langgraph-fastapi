"""
This will handle the business logic for the reporting module, such as fetching data from the database, processing it, and preparing it for the API responses.
"""
from sqlalchemy.orm import Session
from app.modules.reporting.repository import get_job_count


def get_jobs_count(db: Session):
    return {"total_jobs": get_job_count(db)}
