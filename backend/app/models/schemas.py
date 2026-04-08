from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: List[str] = Field(default_factory=list)
    min_experience_years: int = 0


class Job(JobCreate):
    id: str
    created_at: datetime


class ResumeAnalysis(BaseModel):
    extracted_skills: List[str]
    education: List[str]
    experience_years: float
    skill_match_score: float
    missing_skills: List[str]
    suggestions: List[str]


class CandidateCreate(BaseModel):
    full_name: str
    email: str
    target_job_id: Optional[str] = None


class Candidate(BaseModel):
    id: str
    full_name: str
    email: str
    target_job_id: Optional[str] = None
    resume_text: str = ""
    analysis: Optional[ResumeAnalysis] = None
    job_match_score: float = 0.0
    interview_score: float = 0.0
    final_score: float = 0.0
    recommendation: str = "Pending"
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    created_at: datetime


class InterviewMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime


class InterviewSession(BaseModel):
    id: str
    candidate_id: str
    mode: str = "chat"
    round_type: str = "technical"
    questions: List[str] = Field(default_factory=list)
    transcript: List[InterviewMessage] = Field(default_factory=list)
    score: float = 0.0
    created_at: datetime


class CandidateRank(BaseModel):
    candidate_id: str
    name: str
    email: str
    target_job_id: Optional[str]
    final_score: float
    recommendation: str


class InterviewStartRequest(BaseModel):
    candidate_id: str
    mode: str = "chat"
    round_type: str = "technical"


class InterviewAnswerRequest(BaseModel):
    answer: str
