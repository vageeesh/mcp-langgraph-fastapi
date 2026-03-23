from datetime import date
from app.core.database import SessionLocal
from app.modules.reporting.models import (
    Client, Project, Source,
    Job
)


db = SessionLocal()

try:
    client = Client(name="Alchemy Inc")
    db.add(client)
    db.commit()
    db.refresh(client)

    project = Project(
        name="Spectra",
        client_id=client.id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    source_1 = Source(name="Facebook")
    db.add(source_1)
    source_2 = Source(name="Instagram")
    db.add(source_2)

    db.commit()
    db.refresh(source_1)
    db.refresh(source_2)

    job_1 = Job(
        project_id=project.id,
        source_id=source_1.id,
        date=date(2026, 1, 12),
        status="COMPLETED",
        cost=100.0
    )

    job_2 = Job(
        project_id=project.id,
        source_id=source_2.id,
        date=date(2026, 2, 10),
        status="FAILED",
        cost=50.0
    )

    job_3 = Job(
        project_id=project.id,
        source_id=source_2.id,
        date=date(2026, 3, 15),
        status="COMPLETED",
        cost=150.0
    )

    db.add_all([job_1, job_2, job_3])
    db.commit()


finally:
    db.close()

print("Seed data inserted")