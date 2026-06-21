from fastapi import Depends,HTTPException,status
from ..jwt.handler import get_current_user
 

def role_necessary(data:str):
    def role_checker(user:str=Depends(get_current_user)):
        member_roles=user.get("roles") or []
        for role_name in member_roles:
            if role_name in data:
                return user
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized")
    return role_checker


