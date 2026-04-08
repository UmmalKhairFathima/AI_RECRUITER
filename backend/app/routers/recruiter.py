from fastapi import APIRouter, Depends
from ..core.config import get_settings
from ..db.repository import JsonRepository
from ..models.schemas import CandidateRank

router = APIRouter(prefix="/api/recruiter", tags=["recruiter"])


def get_repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(settings.data_file)


@router.get("/ranking", response_model=list[CandidateRank])
def get_ranking(repo: JsonRepository = Depends(get_repo)):
    candidates = repo.list_items("candidates")
    sorted_candidates = sorted(candidates, key=lambda c: c.get("final_score", 0.0), reverse=True)
    return [
        {
            "candidate_id": c["id"],
            "name": c["full_name"],
            "email": c["email"],
            "target_job_id": c.get("target_job_id"),
            "final_score": c.get("final_score", 0.0),
            "recommendation": c.get("recommendation", "Pending"),
        }
        for c in sorted_candidates
    ]
