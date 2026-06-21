import redis 
from redis.exceptions import RedisError
from fastapi import FastAPI ,HTTPException,status
from ...utils.config import setting


def get_redis_client():
    redis_client=redis.Redis(host=setting.REDIS_HOST,
                            port=setting.REDIS_PORT,
                            db=setting.REDIS_DB,
                            decode_responses=True)
    try:
        redis_client.ping()
    except RedisError as e:

        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unable to connect to our Redish {setting.REDIS_HOST}, {e}")
        

    return redis_client


