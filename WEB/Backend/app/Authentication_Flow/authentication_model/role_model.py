from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey
from ...db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum



class Role(Base):
    __tablename__="roles"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,unique=True,nullable=False)

    #realtionship with permission
    role_permission_mappings=relationship("RolePermissionMapping",back_populates="role")

    #realtionship with project 
    member_project_role_mappings=relationship("MemberProjectRoleMapping",back_populates="role")

    #relationship with global member role
    member_role_mappings=relationship("MemberRoleMapping",back_populates="role")
