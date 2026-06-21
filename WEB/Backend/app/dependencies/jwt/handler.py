from fastapi import HTTPException ,status ,Depends 
# from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
# from ...db.base import get_db
# from ...Authentication_Flow.authentication_repo  import repo
from .bearer import decode_access_token
# from ...Authentication_Flow.authentication_repo.repo import get_member_by_id

# oauth2_schemes=OAuth2PasswordBearer(tokenUrl="/auth/login")

# # def get_current_user(token:str=Depends(oauth2_schemes), db: Session = Depends(get_db)):
# #     credential_exceptions=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
# #                                         detail="user not authorized")
# #     data= decode_access_token(token,credential_exceptions)
# #     member_id = data.get("member_id")
    
# #     if member_id is None:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Invalid token",
# #         )
    
# #     member = get_member_by_id(db, member_id)
    
# #     if member is None:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="User not found",
# #         )
        
# #     return member


oauth2schemes=OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str=Depends(oauth2schemes)):
    try:
        return decode_access_token(token)
    except HTTPException as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="user is unauthorized",
                                         headers={"WWW-Authenticate":"Bearer"},
                                         ) from exc
   








