import secrets

from redis import Redis

from .redis import get_redis_client


OTP_EXPIRY_TIME = 60 * 10
OTP_ATTEMPT=3

def otp_key(email: str):
    return f"otp:{email.lower()}"


def generate_otp():
    return str(secrets.randbelow(9000) + 1000)


def save_otp(email: str, otp: str, redis_client: Redis = None):
    client = redis_client or get_redis_client()
    client.setex(otp_key(email), OTP_EXPIRY_TIME, otp)


def get_otp(email: str, redis_client: Redis = None):
    client = redis_client or get_redis_client()
    # incrementer=1
    # if get_otp:
    #     incrementer +=1
    #     if incrementer >=3:
 

    return client.get(otp_key(email))


def otp_ttl(email: str, redis_client: Redis = None):
    client = redis_client or get_redis_client()
    return client.ttl(otp_key(email))


def delete_otp(email: str, redis_client: Redis = None):
    client = redis_client or get_redis_client()
    client.delete(otp_key(email))


def verify_otp(email: str, otp: str, redis_client: Redis = None):
    client = redis_client or get_redis_client()
    key = otp_key(email)
    print(key)
    saved_otp = client.get(key)
    ttl = client.ttl(key)
    print(saved_otp)
    if not saved_otp or ttl <= 0:
        return False
    
    if otp != saved_otp:
        return False
    delete_otp(email, client)
    return True
