from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .routers import jobs, candidates, interviews, recruiter

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


app.include_router(jobs.router)
app.include_router(candidates.router)
app.include_router(interviews.router)
app.include_router(recruiter.router)
