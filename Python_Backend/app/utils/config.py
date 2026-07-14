from pydantic_settings import BaseSettings
from typing import Optional

class Setting(BaseSettings):
    DATABASE_URL:str
    OPENAI_API_KEY:Optional[str]=None
    OPENAI_MODEL:str="gpt-4.1-mini"
    AWS_ACCESS_KEY_ID:Optional[str]=None
    AWS_SECRET_ACCESS_KEY:Optional[str]=None
    AWS_S3_BUCKET_NAME:Optional[str]=None
    AWS_REGION:str="ap-south-1"
    
    class Config:
        env_file=".env"

setting=Setting()
