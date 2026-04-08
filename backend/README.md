# AI Recruiter Platform Backend

## Run

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## API Summary

- `POST /api/jobs` create job
- `GET /api/jobs` list jobs
- `POST /api/candidates` create candidate
- `POST /api/candidates/{candidate_id}/upload-resume` upload resume text/pdf
- `GET /api/candidates` list candidates
- `POST /api/interviews/start` start chat/voice round
- `POST /api/interviews/{session_id}/answer` submit answer and fetch next question
- `GET /api/recruiter/ranking` ranked candidates
