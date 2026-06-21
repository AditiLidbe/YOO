from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey
from ...db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

from ...Project_Flow.project_model.project_model import Project

class SubscriptionEnum(str,Enum):
    ALL_FEATURE="all_feature"
    HALF_FEATURE="half_feature"
    BASIC_FEATURE="basic_feature"

class Company(Base):
    __tablename__="companys"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,unique=True,nullable=False)
    logo=Column(String,nullable=False)
    subcription=Column(SqlEnum(SubscriptionEnum),nullable=False)
    domain=Column(String,unique=True,nullable=False)
    # relationship with member
    members=relationship("Member",back_populates="company")

    # relationship with project
    projects=relationship("Project",back_populates="company")