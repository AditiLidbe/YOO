from fastapi import Header, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from ..model.user_model import UserRole


class GatewayUser(BaseModel):
    id: int
    role: UserRole


def get_gateway_user(
    user_id: Optional[str] = Header(default=None, alias="X-User-Id"),
    role: Optional[str] = Header(default=None, alias="X-Role"),
):
    if user_id is None or role is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required",
        )

    try:
        return GatewayUser(id=int(user_id), role=UserRole(role))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user details from gateway",
        )
