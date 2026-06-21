from fastapi import APIRouter,Depends ,Form , File,UploadFile ,HTTPException,status
from sqlalchemy.orm import Session
from pydantic import EmailStr
from ...db.base import get_db
from ...Authentication_Flow.authentication_model.member_model import Member
from ..company_schema.schema import CompanyOnboarding,AdminActivation ,Companies,CompanyCreate,CompanyUpdate, PresignedRequest,PresignedResponse
from..company_model.company_model import Company,SubscriptionEnum
from ...Authentication_Flow.authentication_service.auth_service import login_with_otp, request_otp
from ...dependencies.jwt.handler import get_current_user
from ..company_service.service import onboarding,activate_company_admin,all_companies,get_company,delete_company,edit_company ,get_all_company
from ...dependencies.RBAC.role_checker import role_necessary
from ..company_service.upload_file import generate_logo_presigned_url
router=APIRouter(prefix="/company",tags=["Company"])

# ,domain=domain
@router.post("/onboard")
def company_onboarding(name:str= Form(...),
                       domain:str=Form(...),
                       logo:str=Form(...),
                       subscription:SubscriptionEnum=Form(...),admin_name:str=Form(...),admin_last_name:str=Form(...),admin_email:EmailStr=Form(...),db:Session=Depends(get_db),user=Depends(role_necessary("SUPER_ADMIN"))) :
    return onboarding(db=db,name=name,domain=domain,logo=logo,subscription=subscription,admin_name=admin_name,admin_last_name=admin_last_name,admin_email=admin_email)
   

@router.post("/logo/presign", response_model=PresignedResponse)
def get_logo_presigned(data: PresignedRequest):
    upload_data = generate_logo_presigned_url("company-logos", data.file_name, data.content_type)
    if upload_data is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create presigned upload")
    return upload_data


@router.post("/activation-admin/")
def active_admin(email:EmailStr=Form(...),otp:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    return activate_company_admin(db,email,otp,password)


@router.get("/all")
def get_all_companies(db: Session = Depends(get_db)):
    return get_all_company(db)


@router.get("/{company_id}")
def get_company_by_id(company_id: int,db: Session = Depends(get_db)):
    return get_company(db, company_id)


@router.patch("/{company_id}")
def update_company_by_id(company_id: int,name:str= Form(...),domain:str=Form(...),logo:str=Form(...),subscription:SubscriptionEnum=Form(...),db: Session = Depends(get_db),user=Depends(role_necessary("SUPER_ADMIN"))):
    return edit_company(db,company_id,name,domain,logo,subscription)

@router.delete("/{company_id}")
def delete_company_by_id(company_id: int,db: Session = Depends(get_db)):
    return delete_company(db, company_id)
