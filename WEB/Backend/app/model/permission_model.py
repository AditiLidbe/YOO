from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

class PermissionEnum(str,Enum):
    CREATE_TASK="create_task"
    UPDATE_TASK="upload_task"
    DELETE_TASK="delete_task"
    ASSIGN_TASK="assign_task"
    MANAGE_PERMISSION="manage_permission"
    INVITE_MEMBERS="invite_members"
    ENABLE_PROGRESS_IN_BUCKET="enable_progress_in_bucket"


class Permission(Base):
    __tablename__="permissions"
    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(SqlEnum(PermissionEnum),nullable=False)

    #realtionship with role and permission
    role_permission_mappings=relationship("RolePermissionMapping",back_populates="permission")

    # realtionship with member and permission
    member_permission_mappings=relationship("MemberPermissionMapping",back_populates="permission")
