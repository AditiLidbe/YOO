from fastapi import HTTPException, status
from redis import Redis
from redis.exceptions import RedisError

from app.utils.config import setting


def get_redis_client():
    client = Redis(
        host=setting.REDIS_HOST,
        port=setting.REDIS_PORT,
        db=setting.REDIS_DB,
        decode_responses=True,
    )
    try:
        client.ping()
    except RedisError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to connect to Redis at {setting.REDIS_HOST}: {exc}",
        ) from exc

    return client
