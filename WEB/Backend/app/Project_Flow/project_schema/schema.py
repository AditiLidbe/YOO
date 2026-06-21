from pydantic import BaseModel, EmailStr, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    company_id: int


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)


class ProjectRead(BaseModel):
    id: int
    name: str
    description: str
    company_id: int

    class Config:
        from_attributes = True


class ProjectInviteCreate(BaseModel):
    email: EmailStr
    role_name: str = Field(min_length=2, max_length=50)


class ProjectInviteAccept(BaseModel):
    email: EmailStr
    token: str


class ProjectInviteSent(BaseModel):
    id: int
    project_id: int
    email: EmailStr
    role_id: int
    status: str

    class Config:
        from_attributes = True
