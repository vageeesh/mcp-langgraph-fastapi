"""
This will handle the database interactions for the reporting module, such as querying for job counts, fetching running jobs, etc.
"""
from sqlalchemy.orm import Session
from .models import Job


def get_job_count(db: Session):

    return db.query(Job).count()


def get_running_jobs(db: Session):

    return db.query(Job).filter(
        Job.status == "IN_PROGRESS"
    ).all()