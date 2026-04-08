from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from ..core.config import get_settings
from ..db.repository import JsonRepository
from ..models.schemas import Candidate, CandidateCreate, ResumeAnalysis
from ..services.resume_analyzer import parse_resume, extract_text_from_resume_file
from ..services.job_matching import compute_job_match_score
from ..services.evaluation_engine import evaluate_candidate

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


def get_repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(settings.data_file)


@router.post("", response_model=Candidate)
def create_candidate(payload: CandidateCreate, repo: JsonRepository = Depends(get_repo)):
    candidate = {
        "id": str(uuid4()),
        "full_name": payload.full_name,
        "email": payload.email,
        "target_job_id": payload.target_job_id,
        "resume_text": "",
        "analysis": None,
        "job_match_score": 0.0,
        "interview_score": 0.0,
        "final_score": 0.0,
        "recommendation": "Pending",
        "strengths": [],
        "weaknesses": [],
        "created_at": datetime.utcnow().isoformat(),
    }
    repo.upsert_item("candidates", candidate)
    return candidate


@router.post("/{candidate_id}/upload-resume", response_model=ResumeAnalysis)
async def upload_resume(
    candidate_id: str,
    resume_file: UploadFile = File(None),
    resume_text: str = Form(""),
    repo: JsonRepository = Depends(get_repo),
):
    candidate = repo.get_item("candidates", candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    text = resume_text
    if resume_file is not None:
        content = await resume_file.read()
        text = extract_text_from_resume_file(content, resume_file.filename or "") or text

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not read resume content. Upload PDF/DOCX/TXT or provide resume text.",
        )

    job = repo.get_item("jobs", candidate.get("target_job_id")) if candidate.get("target_job_id") else None
    required_skills = job.get("required_skills", []) if job else []
    min_exp = job.get("min_experience_years", 0) if job else 0

    analysis = parse_resume(text, required_skills)
    job_match_score = compute_job_match_score(
        candidate_skills=analysis["extracted_skills"],
        job_skills=required_skills,
        experience_years=analysis["experience_years"],
        min_exp=min_exp,
    )

    evaluation = evaluate_candidate(
        skill_match_score=analysis["skill_match_score"],
        job_match_score=job_match_score,
        interview_score=float(candidate.get("interview_score", 0.0)),
    )

    candidate["resume_text"] = text
    candidate["analysis"] = analysis
    candidate["job_match_score"] = job_match_score
    candidate["final_score"] = evaluation["final_score"]
    candidate["strengths"] = evaluation["strengths"]
    candidate["weaknesses"] = evaluation["weaknesses"]
    candidate["recommendation"] = evaluation["recommendation"]

    repo.upsert_item("candidates", candidate)
    return analysis


@router.get("", response_model=list[Candidate])
def list_candidates(repo: JsonRepository = Depends(get_repo)):
    return repo.list_items("candidates")
