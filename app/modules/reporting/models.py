from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from app.core.database import Base


class Client(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Project(Base):

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    client_id = Column(Integer, ForeignKey("clients.id"))


class Source(Base):

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)

    project_id = Column(Integer, ForeignKey("projects.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))

    date = Column(Date)

    status = Column(
        Enum("IN_PROGRESS", "COMPLETED", "FAILED", name="job_status")
    )

    cost = Column(Float)
