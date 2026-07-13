from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import Base, engine
from app.model import AI, AIResult, Application, Candidate, Job, Recruiter, User
from app.router.ai_router import router as ai_router
from app.router.application_router import router as application_router
from app.router.file_router import router as file_router
from app.router.job_router import router as job_router
from app.router.router import router as module_one_router


app = FastAPI(title="Talenta Backend")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(module_one_router)
app.include_router(job_router)
app.include_router(application_router)
app.include_router(ai_router)
app.include_router(file_router)
