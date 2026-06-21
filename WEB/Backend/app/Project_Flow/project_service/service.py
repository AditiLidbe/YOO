from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ...Authentication_Flow.authentication_model.member_model import Member
from ...Authentication_Flow.authentication_service.email_service import send_email
from ..project_model.member_project_role_mapping_model import MemberProjectRoleMapping

from ...utils.loggers import logger

from ..project_repo.repo import create_default_buckets,create_project,create_project_invite,delete_project,get_member_by_email,get_member_by_id,get_project_by_id,get_project_by_name,get_project_invite_by_token,get_projects,get_role_by_name,update_project,



def can_manage_projects(current_user: dict):
    roles = current_user.get("roles") or []
    return "ADMIN" in roles


def list_projects(
    db: Session,
    company_id: int | None = None,
    search: str | None = None,
    sort_by: str = "name",
    sort_order: str = "desc",
):
    return get_projects(
        db=db,
        company_id=company_id,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


def create_project_service(
    db: Session,
    name: str,
    current_user:dict,
    description: str,
    company_id: int,
):

    member = get_member_by_id(db, current_user.get("member_id"))
    if member is not None and member.company_id != company_id and "SUPER_ADMIN" not in (current_user.get("roles") or []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create projects for your company",
        )

    if get_project_by_name(db, name):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Project already exists",
        )

    project = create_project(db, name=name, description=description, company_id=company_id)
    create_default_buckets(db, project.id)
    db.commit()
    db.refresh(project)
    return {"message": "Project created successfully", "project": project}


def edit_project_service(
    db: Session,
    current_user: dict,
    project_id: int,
    name: str | None = None,
    description: str | None = None,
):
    if not can_manage_projects(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or super admin can edit projects",
        )

    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    if name is not None and name != project.name:
        existing_project = get_project_by_name(db, name)
        if existing_project is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Project name already exists",
            )

    update_project(db, project, name=name, description=description)
    db.commit()
    db.refresh(project)
    return {"message": "Project updated successfully", "project": project}


def delete_project_service(db: Session, project_id: int): # current_user: dict
    if not can_manage_projects(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or super admin can delete projects",
        )

    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    member = get_member_by_id(db, current_user.get("member_id"))
    if member is not None and member.company_id != project.company_id and "SUPER_ADMIN" not in (current_user.get("roles") or []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete projects from your company",
        )

    delete_project(db, project)
    db.commit()
    return {"message": "Project deleted successfully"}


def invite_member_service(
    db: Session,
    current_user: dict,
    project_id: int,
    email: str,
    role_name: str,
):
    if not can_manage_projects(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin or super admin can invite members",
        )

    project = get_project_by_id(db, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    member = get_member_by_id(db, current_user.get("member_id"))
    if member is not None and member.company_id != project.company_id and "SUPER_ADMIN" not in (current_user.get("roles") or []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only invite members to your company projects",
        )

    role = get_role_by_name(db, role_name)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    member = get_member_by_email(db, email)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    token = uuid4().hex
    invite = create_project_invite(
        db=db,
        project_id=project_id,
        email=email,
        role_id=role.id,
        # invited_by=current_user.get("member_id"),
        token=token,
    )

    link = f"http://localhost:5173/project-invite?token={token}&email={email}"
    send_email(
        email,
        "Project invite",
        f"You were invited to project {project.name}. Open this link: {link}",
    )

    db.commit()
    return {
        "message": "Invite sent successfully",
        "invite_id": invite.id,
        "token": token,
    }

