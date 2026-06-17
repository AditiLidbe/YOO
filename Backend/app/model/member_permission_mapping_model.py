from sqlalchemy import Column, String,Integer,Enum as SqlEnum ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

class MPStatusEnum(str,Enum):
    GRANT="grant"
    REVOKE="revoke"


class MemberPermissionMapping(Base):
    __tablename__="member_permission_mapping"
    id=Column(Integer,primary_key=True,nullable=False)
    action=Column(SqlEnum(MPStatusEnum),nullable=False)

    #relationship with member
    member_id=Column(Integer,ForeignKey("members.id"),nullable=False)
    member=relationship("Member",back_populates="permission_mappings")

    #relationship with permission
    permission_id=Column(Integer,ForeignKey("permissions.id"),nullable=False)
    permission=relationship("Permission",back_populates="member_permission_mappings")

    