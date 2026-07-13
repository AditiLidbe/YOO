from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt

from app.schema.user_schema import TokenData
from app.utils.config import setting


def create_access_token(data: dict):
    token_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_data.update({"exp": expire, "token_type": "access"})
    return jwt.encode(token_data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)


def create_refresh_token(data: dict):
    token_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=setting.REFRESH_TOKEN_EXPIRE_DAYS
    )
    token_data.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(token_data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)


def verify_token(token: str, expected_token_type: str = "access"):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not able to verify token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            setting.SECRET_KEY,
            algorithms=[setting.ALGORITHM],
        )
        user_id = payload.get("user_id")
        email = payload.get("email")
        role = payload.get("role")
        token_type = payload.get("token_type")

        if (
            user_id is None
            or email is None
            or role is None
            or token_type != expected_token_type
        ):
            raise credentials_exception

        return TokenData(id=user_id, email=email, role=role)
    except JWTError as exc:
        raise credentials_exception from exc
