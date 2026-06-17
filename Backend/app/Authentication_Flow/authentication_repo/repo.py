from sqlalchemy.orm import Session
from ..authentication_model.member_model import Member


def get_member_by_email(email: str, db: Session):
    print(email)
    return db.query(Member).filter(Member.email == email).first()


def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.member_id == member_id).first()


def get_member_role(member: Member):
    if member.role_mappings:
        first_mapping = member.role_mappings[0]
        return first_mapping.role.name

    if not member.project_role_mappings:
        return None

    first_mapping = member.project_role_mappings[0]
    return first_mapping.role.name

