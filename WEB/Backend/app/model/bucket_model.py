from sqlalchemy import Column, String,Integer ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship


     
class Bucket(Base):
    __tablename__="buckets"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,unique=True,nullable=False)

    # relationship with task 
    tasks=relationship("Task",back_populates="bucket")

    #realtionship with project
    project_id=Column(Integer,ForeignKey("projects.id"),nullable=False)
    project=relationship("Project",back_populates="bucket")
