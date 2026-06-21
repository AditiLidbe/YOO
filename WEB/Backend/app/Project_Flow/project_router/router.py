from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.dependencies.RBAC.role_checker import role_necessary

from ..project_schema.schema import (
    ProjectCreate,
    ProjectInviteAccept,
    ProjectInviteCreate,
    ProjectUpdate,
)
from ..project_service.service import (
    accept_project_invite_service,
    archive_project_service,
    create_project_service,
    edit_project_service,
    hard_delete_project_service,
    invite_member_service,
    list_projects,
    soft_delete_project_service,
    unarchive_project_service,
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("")
def create_project(data: ProjectCreate,current_user: dict = Depends(role_necessary("ADMIN")),db: Session = Depends(get_db),):
    return create_project_service(
        db=db,
        current_user=current_user,
        name=data.name,
        description=data.description,
        company_id=data.company_id,
    )


@router.get("")
def get_projects(
    company_id: int | None = Query(default=None),
    search: str | None = Query(default=None),
    include_archived: bool = Query(default=False),
    sort_by: str = Query(default="name"),
    sort_order: str = Query(default="asc"),
    limit: int | None = Query(default=None),
    offset: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return list_projects(
        db=db,
        company_id=company_id,
        search=search,
        include_archived=include_archived,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


@router.patch("/{project_id}")
def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: dict = Depends(role_necessary("SUPER_ADMIN", "ADMIN")),
    db: Session = Depends(get_db),
):
    return edit_project_service(
        db=db,
        current_user=current_user,
        project_id=project_id,
        name=data.name,
        description=data.description,
    )


@router.delete("/{project_id}")
def remove_project(
    project_id: int,
    current_user: dict = Depends(role_necessary("ADMIN")),
    db: Session = Depends(get_db),
):
    return soft_delete_project_service(db=db, current_user=current_user, project_id=project_id)


@router.patch("/{project_id}/archive")
def archive_project(
    project_id: int,
    current_user: dict = Depends(role_necessary("ADMIN")),
    db: Session = Depends(get_db),
):
    return archive_project_service(db=db, current_user=current_user, project_id=project_id)


@router.patch("/{project_id}/unarchive")
def unarchive_project(
    project_id: int,
    current_user: dict = Depends(role_necessary("ADMIN")),
    db: Session = Depends(get_db),
):
    return unarchive_project_service(db=db, current_user=current_user, project_id=project_id)


@router.delete("/{project_id}/hard")
def hard_delete_project(
    project_id: int,
    current_user: dict = Depends(role_necessary("ADMIN")),
    db: Session = Depends(get_db),
):
    return hard_delete_project_service(db=db, current_user=current_user, project_id=project_id)


@router.post("/{project_id}/invite")
def invite_member(
    project_id: int,
    data: ProjectInviteCreate,
    current_user: dict = Depends(role_necessary("ADMIN")),
    db: Session = Depends(get_db),
):
    return invite_member_service(
        db=db,
        current_user=current_user,
        project_id=project_id,
        email=data.email,
        role_name=data.role_name,
    )


@router.post("/invite/accept")
def accept_invite(data: ProjectInviteAccept, db: Session = Depends(get_db)):
    return accept_project_invite_service(db=db, email=data.email, token=data.token)
