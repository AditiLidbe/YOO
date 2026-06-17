from fastapi import APIRouter,Depends ,Form , File,UploadFile
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.db.base import get_db
from ...Authentication_Flow.authentication_model.member_model import Member
from ..company_schema.schema import CompanyOnboarding,AdminActivation ,Companies,CompanyCreate,CompanyUpdate, PresignedRequest,PresignedResponse
from..company_model.company_model import Company,SubscriptionEnum
from ...Authentication_Flow.authentication_service.auth_service import login_with_otp, request_otp
from ...dependencies.jwt.handler import get_current_user
from ..company_service.service import onboarding,activate_company_admin,all_companies,get_company,delete_company
# from ...dependencies.RBAC.role_checker import role_necessary

router=APIRouter(prefix="/company",tags=["Company"])

# user:Member=Depends(get_current_user)
@router.post("/onboard")
def company_onboarding(name:str= Form(...),
                       domain:str=Form(...),
                       logo:str=Form(...),
                       subscription:SubscriptionEnum=Form(...),admin_name:str=Form(...),admin_last_name:str=Form(...),admin_email:EmailStr=Form(...),db:Session=Depends(get_db)) :
    return onboarding(db=db,name=name,domain=domain,logo=logo,subscription=subscription,admin_name=admin_name,admin_last_name=admin_last_name,admin_email=admin_email)
   

@router.post("/activation-admin/")
def active_admin(email:EmailStr=Form(...),otp:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    return activate_company_admin(db,email,otp,password)

#esponse_model=list[Companies]
@router.get("/all")
def get_all_companies(db: Session = Depends(get_db)):
    return all_companies(db)

# , response_model=Companies
@router.get("/{company_id}")
def get_company_by_id(company_id: int,db: Session = Depends(get_db)):
    return get_company(db, company_id)


# @router.patch("/{company_id}", response_model=Company)
# def update_company_by_id(company_id: int,data: CompanyUpdate,db: Session = Depends(get_db)):
#     return edit_company(db, company_id, data)


# user: Member = Depends(role_necessary(["SUPER_ADMIN"])),
@router.delete("/{company_id}")
def delete_company_by_id(company_id: int,db: Session = Depends(get_db)):
    return delete_company(db, company_id)
