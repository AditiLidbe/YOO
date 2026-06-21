from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Authentication_Flow.authentication_router.router import router as AuthRouter
from app.Company_Onboarding.company_router.router import router as CompnayRouter


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

app.include_router(AuthRouter)  
app.include_router(CompnayRouter)

