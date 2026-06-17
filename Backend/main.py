from fastapi import FastAPI

from app.Authentication_Flow.authentication_router import router as AuthRouter
from app.Company_Onboarding.company_router import router as CompnayRouter
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

app.include_router(AuthRouter.router)  
app.include_router(CompnayRouter.router)

