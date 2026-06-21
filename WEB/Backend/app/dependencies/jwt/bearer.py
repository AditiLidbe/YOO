from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from ...db.base import get_db
# from Backend.app.Authentication_Flow.authentication_model.member_model import Member
from ...Authentication_Flow.authentication_model.member_model import Member
from ...utils.config import setting


ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(member: Member, role: str ):
    private_key = open(setting.PRIVATE_KEY_PATH).read()
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES 
    )

    data = {
        "member_id": member.id,
        "email": member.email,
        "role": role,
        "exp": expire_time,
    }

    return jwt.encode(data, private_key, algorithm=ALGORITHM)


def decode_access_token(token: str):
    public_key = open(setting.PUBLIC_KEY_PATH).read()

    try:
        return jwt.decode(token, public_key, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# def get_current_member(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db),
# ):
#     try:
#         payload = decode_access_token(token)
#         member = db.query(Member).filter(Member.id == payload.get("member_id")).first()

#         if member is None:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Member not found",
#             )

#         return member
#     except Exception as exc:
#         return f"Exception kya hai {exc}"
