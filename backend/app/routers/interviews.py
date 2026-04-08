from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from ..core.config import get_settings
from ..db.repository import JsonRepository
from ..models.schemas import InterviewSession, InterviewStartRequest, InterviewAnswerRequest
from ..services.interview_engine import generate_questions, score_answer
from ..services.evaluation_engine import evaluate_candidate

router = APIRouter(prefix="/api/interviews", tags=["interviews"])


def get_repo() -> JsonRepository:
    settings = get_settings()
    return JsonRepository(settings.data_file)


@router.post("/start", response_model=InterviewSession)
def start_interview(payload: InterviewStartRequest, repo: JsonRepository = Depends(get_repo)):
    candidate = repo.get_item("candidates", payload.candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    job_title = "the role"
    if candidate.get("target_job_id"):
        job = repo.get_item("jobs", candidate["target_job_id"])
        if job:
            job_title = job.get("title", "the role")

    questions = generate_questions(job_title, payload.round_type)
    session = {
        "id": str(uuid4()),
        "candidate_id": payload.candidate_id,
        "mode": payload.mode,
        "round_type": payload.round_type,
        "questions": questions,
        "transcript": [
            {
                "role": "interviewer",
                "content": questions[0],
                "timestamp": datetime.utcnow().isoformat(),
            }
        ],
        "score": 0.0,
        "created_at": datetime.utcnow().isoformat(),
    }
    repo.upsert_item("interviews", session)
    return session


@router.post("/{session_id}/answer", response_model=InterviewSession)
def submit_answer(session_id: str, payload: InterviewAnswerRequest, repo: JsonRepository = Depends(get_repo)):
    session = repo.get_item("interviews", session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    idx = len([m for m in session["transcript"] if m["role"] == "candidate"])
    current_question = session["questions"][min(idx, len(session["questions"]) - 1)]
    expected_keywords = current_question.lower().replace("?", "").split()[:5]

    ans_score = score_answer(payload.answer, expected_keywords)
    prev_count = idx
    session["score"] = round(((session["score"] * prev_count) + ans_score) / (prev_count + 1), 2)

    session["transcript"].append({
        "role": "candidate",
        "content": payload.answer,
        "timestamp": datetime.utcnow().isoformat(),
    })

    next_idx = idx + 1
    if next_idx < len(session["questions"]):
        session["transcript"].append({
            "role": "interviewer",
            "content": session["questions"][next_idx],
            "timestamp": datetime.utcnow().isoformat(),
        })

    repo.upsert_item("interviews", session)

    candidate = repo.get_item("candidates", session["candidate_id"])
    if candidate:
        candidate["interview_score"] = session["score"]
        skill_match = candidate.get("analysis", {}).get("skill_match_score", 0.0) if candidate.get("analysis") else 0.0
        eval_data = evaluate_candidate(skill_match, candidate.get("job_match_score", 0.0), session["score"])
        candidate["final_score"] = eval_data["final_score"]
        candidate["strengths"] = eval_data["strengths"]
        candidate["weaknesses"] = eval_data["weaknesses"]
        candidate["recommendation"] = eval_data["recommendation"]
        repo.upsert_item("candidates", candidate)

    return session
