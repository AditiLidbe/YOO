from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from  app.db.base import get_db
from ..authentication_schema.auth_schema import Request,Verify,MemberLogin
from ..authentication_service.auth_service import login_with_otp, request_otp 
from ..authentication_service.auth_service import login_member


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/request-otp")
def request_member_otp(data:Request, db: Session = Depends(get_db)):
        return request_otp(data.email, db)

@router.post("/verify-otp")
def verify_member_otp(data:Verify, db: Session = Depends(get_db)):
    return login_with_otp(data.email, data.otp, db)


# for backend 
@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    data=MemberLogin(email=form_data.username,password=form_data.password)
    return login_member(data, db)

