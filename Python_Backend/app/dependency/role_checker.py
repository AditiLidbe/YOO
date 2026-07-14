from fastapi import Depends, HTTPException, status

from .gateway_user import GatewayUser, get_gateway_user


def role_necessary(allowed_roles):
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def only_role(user: GatewayUser = Depends(get_gateway_user)):
        if user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions."
            )
        return user

    return only_role
