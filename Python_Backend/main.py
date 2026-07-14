from fastapi import FastAPI

from app.router.job_router import router as job_router
from app.router.application_router import router as application_router
from app.router.ai_router import router as ai_router


app=FastAPI()

app.include_router(job_router)
app.include_router(application_router)
app.include_router(ai_router)


@app.get("/")
def home():
    return {"message":"Python backend is running"}
