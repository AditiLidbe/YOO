from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ...db.base import Base


class MemberRoleMapping(Base):
    __tablename__ = "member_role_mapping"

    id = Column(Integer, primary_key=True, nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    member = relationship("Member", back_populates="role_mappings")
    role = relationship("Role", back_populates="member_role_mappings")
