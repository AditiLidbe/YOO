from pydantic import BaseModel,EmailStr,Field
from ..company_model.company_model import SubscriptionEnum
class CompanyOnboarding(BaseModel):
    name: str = Field(..., pattern=r"^(?i)[A-Z]+$")
    domain:str=Field(...,pattern=r"^[a-zA-Z0-9-]+\.com$")
    admin_name:str = Field(..., pattern=r"^(?i)[A-Z]+$")
    admin_last_name:str = Field(..., pattern=r"^(?i)[A-Z]+$")
    admin_email:EmailStr
    subscription:SubscriptionEnum
    # message:str
    # company_id:int
    # admin_id:int

class AdminActivation(BaseModel):
    email:EmailStr
    otp:str
    password:str


class PresignedRequest(BaseModel):
    file_name: str = Field(min_length=1)
    content_type: str = Field(min_length=1)


class PresignedResponse(BaseModel):
    url: str
    fields: dict[str, str]
    key: str


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    domain: str = Field(min_length=3, max_length=100)
    logo: str = Field(min_length=1)
    subscription: SubscriptionEnum


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    domain: str | None = Field(default=None, min_length=3, max_length=100)
    logo: str | None = Field(default=None, min_length=1)
    subscription: SubscriptionEnum | None = None


class Companies(BaseModel):

    id: int
    name: str
    domain: str
    logo: str
    subscription: SubscriptionEnum

    class Config:
        from_attributes=True
