from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from frontend.Backend.app.Authentication_Flow.authentication_model.member_model import Member
from frontend.Backend.app.Authentication_Flow.authentication_model.role_model import Role
from frontend.Backend.app.model.bucket_model import Bucket
from app.model.project_invite_model import ProjectInvite
from app.model.project_model import Project


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_project_by_name(db: Session, name: str):
    return db.query(Project).filter(Project.name == name).first()


def get_projects(
    db: Session,
    company_id: int | None = None,
    search: str | None = None,
    sort_by: str = "id",
    sort_order: str = "desc",
):
    query = db.query(Project)

    if company_id is not None:
        query = query.filter(Project.company_id == company_id)

    if search:
        search_text = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Project.name.ilike(search_text),
                Project.description.ilike(search_text),
            )
        )

    sort_columns = {
        "id": Project.id,
        "name": Project.name,
        "company_id": Project.company_id,
    }
    sort_column = sort_columns.get(sort_by, Project.id)

    if sort_order.lower() == "asc":
        query = query.order_by(asc(sort_column))
    else:
        query = query.order_by(desc(sort_column))

    return query.all()


def create_project(db: Session, name: str, description: str, company_id: int):
    project = Project(name=name, description=description, company_id=company_id)
    db.add(project)
    db.flush()
    return project


def update_project(db: Session, project: Project, name: str | None = None, description: str | None = None):
    if name is not None:
        project.name = name

    if description is not None:
        project.description = description

    db.flush()
    return project


def delete_project(db: Session, project: Project):
    db.delete(project)
    db.flush()


def create_default_buckets(db: Session, project_id: int):
    bucket_names = ["To Do", "In Progress", "QA", "Completed"]
    buckets = []

    for bucket_name in bucket_names:
        bucket = Bucket(name=f"{project_id}-{bucket_name}", project_id=project_id)
        db.add(bucket)
        buckets.append(bucket)

    db.flush()
    return buckets


def get_member_by_email(db: Session, email: str):
    return db.query(Member).filter(Member.email == email).first()


def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def create_project_invite(
    db: Session,
    project_id: int,
    email: str,
    role_id: int,
    invited_by: int,
    token: str,
):
    invite = ProjectInvite(
        project_id=project_id,
        email=email,
        role_id=role_id,
        invited_by=invited_by,
        token=token,
    )
    db.add(invite)
    db.flush()
    return invite


def get_project_invite_by_token(db: Session, token: str):
    return db.query(ProjectInvite).filter(ProjectInvite.token == token).first()
