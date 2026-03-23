from pydantic import BaseModel
from datetime import date


class JobResponse(BaseModel):

    id: int
    project_id: int
    source_id: int
    date: date
    status: str
    cost: float


class JobCountResponse(BaseModel):

    total_jobs: int
