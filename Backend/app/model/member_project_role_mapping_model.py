from sqlalchemy import Column,Integer ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship



class MemberProjectRoleMapping(Base):
    __tablename__="member_project_role_mapping"
    id=Column(Integer,primary_key=True,nullable=False)

   
    #relationship with role
    role_id=Column(Integer,ForeignKey("roles.id"),nullable=False)
    role=relationship("Role",back_populates="member_project_role_mappings")

    #relationship with member
    member_id=Column(Integer,ForeignKey("members.id"),nullable=False)
    member=relationship("Member",back_populates="project_role_mappings")

    #relationship with project
    project_id=Column(Integer,ForeignKey("projects.id"),nullable=False)
    project=relationship("Project",back_populates="member_role_mappings")

    