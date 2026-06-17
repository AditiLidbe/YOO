from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DATABASE_URL:str
    SECRET_KEY:str

    AWS_S3_BUCKET_NAME:str
    AWS_SECRET_KEY_ID:str
    AWS_SECRET_ACCESS_KEY:str
    AWS_REGION:str
    SES_FROM_EMAIL:str

    REDIS_HOST:str
    REDIS_PORT:str
    REDIS_DB :int


    PRIVATE_KEY_PATH: str = "private_key.pem"
    PUBLIC_KEY_PATH: str = "public_key.pem"
    
    class Config:
        env_file=r"app\__gitignore__\.env"

setting=Setting()