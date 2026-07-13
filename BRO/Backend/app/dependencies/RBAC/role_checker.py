from fastapi import Depends, HTTPException, status

from app.dependencies.jwt.handler import get_current_user


def role_necessary(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        user_role = user.role.value if hasattr(user.role, "value") else user.role
        if user_role == required_role:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    return role_checker
