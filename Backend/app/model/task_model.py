from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey,TIMESTAMP
from ..db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

class TaskStatusEnum(str,Enum):
    PENDING="pending"
    COMPLETED="completed"
    IN_PROGRESS="in_progress"

class Task(Base):
    __tablename__="tasks"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,unique=True,nullable=False)
    status=Column(SqlEnum(TaskStatusEnum),default=TaskStatusEnum.PENDING,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())

    #relationship with project 
    project_id=Column(Integer,ForeignKey("projects.id"),nullable=False)
    project=relationship("Project",back_populates="tasks")


    # relationship with member
    creator_id=Column(Integer,ForeignKey("members.id"),nullable=False)
    created_by=relationship("Member",back_populates="tasks")

    # relationship with bucket
    bucket_id=Column(Integer,ForeignKey("buckets.id"),nullable=False)
    bucket=relationship("Bucket",back_populates="tasks")
    
    #relationship with comment 
    comments=relationship("Comment",back_populates="task")

    #relationship with assigned member 
    member_mappings=relationship("MemberTaskMapping",back_populates="task")
