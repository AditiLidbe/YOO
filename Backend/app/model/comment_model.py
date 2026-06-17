from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey ,TIMESTAMP
from ..db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from enum import Enum

class Comment(Base):
    __tablename__="comments"
    id=Column(Integer,primary_key=True,nullable=False)
    description=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    
    # relationship with member 
    member_id=Column(Integer,ForeignKey("members.id"),nullable=False)
    member=relationship("Member",back_populates="comments")

    # relationship with task
    task_id=Column(Integer,ForeignKey("tasks.id"),nullable=False)
    task=relationship("Task",back_populates="comments")

    