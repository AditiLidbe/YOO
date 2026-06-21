from sqlalchemy import Column,Integer ,ForeignKey
from ..db.base import Base
from sqlalchemy.orm import relationship



class MemberTaskMapping(Base):
    __tablename__="member_task_mapping"
    id=Column(Integer,primary_key=True,nullable=False)

    #relationship with member
    member_id=Column(Integer,ForeignKey("members.id"),nullable=False)
    member=relationship("Member",back_populates="task_mappings")
   
    #relationship with task
    task_id=Column(Integer,ForeignKey("tasks.id"),nullable=False)
    task=relationship("Task",back_populates="member_mappings")