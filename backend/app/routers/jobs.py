from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends
from ..core.config import get_settings
from ..db.repository import JsonRepository
from ..models.schemas import Job, JobCreate

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


def get_repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(settings.data_file)


@router.post("", response_model=Job)
def create_job(payload: JobCreate, repo: JsonRepository = Depends(get_repo)):
    job = {
        "id": str(uuid4()),
        "title": payload.title,
        "description": payload.description,
        "required_skills": payload.required_skills,
        "min_experience_years": payload.min_experience_years,
        "created_at": datetime.utcnow().isoformat(),
    }
    repo.upsert_item("jobs", job)
    return job


@router.get("", response_model=list[Job])
def list_jobs(repo: JsonRepository = Depends(get_repo)):
    return repo.list_items("jobs")
