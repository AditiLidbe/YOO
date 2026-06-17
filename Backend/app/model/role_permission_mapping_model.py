from sqlalchemy import Column,Integer ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship



class RolePermissionMapping(Base):
    __tablename__="role_permission_mapping"
    id=Column(Integer,primary_key=True,nullable=False)

    #relationship with role
    role_id=Column(Integer,ForeignKey("roles.id"),nullable=False)
    role=relationship("Role",back_populates="role_permission_mappings")
   
    #relationship with permission
    permission_id=Column(Integer,ForeignKey("permissions.id"),nullable=False)
    permission=relationship("Permission",back_populates="role_permission_mappings")