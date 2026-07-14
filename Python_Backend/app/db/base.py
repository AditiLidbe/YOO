from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine
from ..utils.config import setting
from ..utils.logger import logger
from sqlalchemy.ext.declarative import declarative_base

connect_args={}
if setting.DATABASE_URL.startswith("sqlite"):
    connect_args={"check_same_thread":False}

engine=create_engine(setting.DATABASE_URL,connect_args=connect_args)
Base=declarative_base()

Session=sessionmaker(autoflush=False,autocommit=False,bind=engine)

logger.info("Session begins")

def get_db():
    db=Session()
    try:
        yield db
    finally:
        logger.info("SESSION CLOSED")
        db.close()
