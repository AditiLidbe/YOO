from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey
from ...db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum
from ...model.comment_model import Comment
from ...model.task_model import Task
from ...Company_Onboarding.company_model.company_model import Company
from ...Project_Flow.project_model.member_project_role_mapping_model import MemberProjectRoleMapping
from ...model.member_permission_mapping_model import MemberPermissionMapping
from ...model.member_task_mapping_model import MemberTaskMapping
from .member_role_mapping_model import MemberRoleMapping
class StatusEnum(str,Enum):
    ACTIVE="active"
    PENDING="pending"


class Member(Base):
    __tablename__="members"
    id=Column(Integer,primary_key=True,nullable=False)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String,unique=True,nullable=False)
    status=Column(SqlEnum(StatusEnum),nullable=False,default=StatusEnum.PENDING)
    password=Column(String,nullable=True)

    #relationship with comment 
    comments=relationship("Comment",back_populates="member")

    #relationship with task
    tasks=relationship("Task",back_populates="created_by")
    
    #relationship with company
    company_id=Column(Integer,ForeignKey("companys.id"),nullable=False)
    company=relationship("Company",back_populates="members")

    #relationship with project role mapping
    project_role_mappings=relationship("MemberProjectRoleMapping",back_populates="member")

    #relationship with permission mapping
    permission_mappings=relationship("MemberPermissionMapping",back_populates="member")

    #relationship with task mapping
    task_mappings=relationship("MemberTaskMapping",back_populates="member")

    #relationship with role mapping
    role_mappings=relationship("MemberRoleMapping",back_populates="member")