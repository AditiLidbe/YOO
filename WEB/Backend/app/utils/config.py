from pydantic_settings import BaseSettings
import os

class Setting(BaseSettings):
    DATABASE_URL:str = os.getenv("DATABASE_URL")
    SECRET_KEY:str = os.getenv("SECRET_KEY")

    AWS_S3_BUCKET_NAME:str = os.getenv("AWS_S3_BUCKET_NAM")
    AWS_SECRET_KEY_ID:str = os.getenv("AWS_SECRET_KEY_ID")
    AWS_SECRET_ACCESS_KEY:str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION:str = os.getenv("AWS_REGION")
    SES_FROM_EMAIL:str = os.getenv("SES_FROM_EMAIL")

    REDIS_HOST:str = os.getenv("REDIS_HOST")
    REDIS_PORT:str = os.getenv("REDIS_PORT")
    REDIS_DB :int = os.getenv("REDIS_DB")


    PRIVATE_KEY_PATH: str = "private_key.pem"
    PUBLIC_KEY_PATH: str = "public_key.pem"
    
    SUPER_ADMIN_EMAIL:str = os.getenv("SUPER_ADMIN_EMAI")
    class Config:
        env_file=r"app\__gitignore__\.env"
        
        model_config = {
            'env_file' : '.env'
        }

setting=Setting()