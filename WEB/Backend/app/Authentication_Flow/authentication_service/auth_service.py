from sqlalchemy.orm import Session
from .email_service import send_otp_email
from fastapi import HTTPException,status
from ..authentication_schema.auth_schema import MemberLogin
from .redis import get_redis_client 
from ..authentication_model.member_model import Member
from .otp_service import generate_otp,delete_otp,save_otp,verify_otp
from ..authentication_repo.repo import get_member_by_email ,get_member_role
from ...dependencies.jwt.bearer import create_access_token
from ...utils.hashing import verify


def request_otp(email, db:Session):
    redis_client=None
    try:
        member= get_member_by_email(email, db)
        if member is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Mmeber not found")
        
        otp=generate_otp()
        redis_client=get_redis_client()
        save_otp(email,otp,redis_client)

    
        send_otp_email(email,otp)
    except Exception as e:
        print(f"Exception AYA {e}")
        delete_otp(email,redis_client)
        return {"message":"Error Aya"}
        
    return {"message":"OTP sent"}


def login_with_otp(email:str,otp:str,db:Session):
    member= get_member_by_email(email,db)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Mmeber not found")
    if not verify_otp(email,otp):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid otp")
   
    role=get_member_role(member)
    if member.project_role_mappings:
        role = member.project_role_mappings[0].role.name
    
    access_token = create_access_token(member, role)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "role": role,
        "token_type": "bearer",
    }

# Swagger Authorize
def valid_passwrod(plain_password:str,hashed_password:str):
    try:
        return  verify(plain_password,hashed_password)
    except Exception:
        return False

    

def login_member(data: MemberLogin, db: Session):
    member =  get_member_by_email(data.email, db)
    
    if not member :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    if not member.password:
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is not set for this account",
        )
    if not valid_passwrod(data.password,member.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not a valid password",
        )

    
    role=get_member_role(member)
    if member.project_role_mappings:
        role = member.project_role_mappings[0].role.name
    
    access_token = create_access_token( member,role)
    return {"access_token": access_token, "token_type": "bearer","email":member.email,"roles":role}
