import os

from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./talenta.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-in-env")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    AWS_S3_BUCKET_NAME: str | None = os.getenv("AWS_S3_BUCKET_NAME")
    AWS_SECRET_KEY_ID: str | None = os.getenv("AWS_SECRET_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str | None = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    SES_FROM_EMAIL: str | None = os.getenv("SES_FROM_EMAIL")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

    SUPER_ADMIN_EMAIL: str | None = os.getenv("SUPER_ADMIN_EMAIL")
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    class Config:
        env_file = ".env"
        extra = "ignore"


setting = Setting()
