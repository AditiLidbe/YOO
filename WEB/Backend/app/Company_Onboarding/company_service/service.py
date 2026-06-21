import boto3
from botocore.exceptions import BotoCoreError,ClientError
from pydantic import EmailStr , Field 
from ...utils.loggers import logger
from sqlalchemy.orm import Session
from ...Authentication_Flow.authentication_model.member_model import Member
from fastapi import HTTPException,Depends ,UploadFile,File , status
from ...Authentication_Flow.authentication_service.email_service import send_email, send_actvation_link_email
from ...Authentication_Flow.authentication_service.redis import get_redis_client
from ...Authentication_Flow.authentication_service.otp_service import generate_otp,get_otp,save_otp,verify_otp
from ...Authentication_Flow.authentication_model.member_model import StatusEnum ,Member
from ..company_model.company_model import SubscriptionEnum
from ..company_repo.repo import create_company,get_member_by_email, get_role_by_name,create_company_admin, assign_role_to_member ,get_company_by_name ,get_company_by_domain,get_companies_by_asc,get_compnaies,get_companies_by_id ,delete_company_by_id,update_company_fields,get_all_companies
from ...utils.config import setting
from ...utils.hashing import hash
# from .upload_file import uplaod_file



logger.info("Company Onboarding")

def if_super_admin(member: Member):
    for mapping in member.role_mappings:
        if mapping.role.name == "SUPER_ADMIN":
            return True

    return False

def onboarding( db: Session,
               name: str,
               domain:str,
               subscription: SubscriptionEnum,
               admin_name: str,
               admin_last_name:str,
               admin_email: EmailStr,
               logo: str,
               ):
    try:
        if not if_super_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Only superadmin can oerform the onbaording")
        
        if get_company_by_name(db,name=name):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Cpompany alredy exists")
        
        if get_company_by_domain(db,domain=domain):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Domain alredy exists")
       
        if get_member_by_email(db,email=admin_email):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Already registered..")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Either admin , company exist domain or the member is not superadmin {exc}",
        )from exc

    # try:
    #     file_bytes=logo.file.read()
    # except Exception as exc:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Coulf not read file {exc}",
    #     )from exc
    # if not file_bytes:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         details="File got nothing",
    #                         )
    
    # s3_client=boto3.client(
    #     's3',
    #     aws_access_key_id=setting.AWS_SECRET_KEY_ID, 
    #     aws_secret_access_key=setting.AWS_SECRET_ACCESS_KEY, 
    #     region_name=setting.AWS_REGION
    # )
    # file_name=f"{name}_{logo.filename}"
    # file_url=f"https://{setting.AWS_S3_BUCKET_NAME}.s3.{setting.AWS_REGION}.amazonaws.com/{file_name}"
    # try:
    #     s3_client.upload_fileobj(
    #         logo.file,
    #         setting.AWS_S3_BUCKET_NAME,
    #         file_name,
    #         ExtraArgs={
    #             "ContentType":logo.content_type
    #         }
    #     )
    # except (BotoCoreError,ClientError) as exc:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                         detail=f"Coulf nor upload image to s3 {exc}") from exc
    
    # logo_path = uplaod_file(file_path, s3_object_name)


    company = create_company(db, name=name, domain=domain,logo=logo, subscription=subscription) #logo=logo_path
    admin = create_company_admin(db,first_name=admin_name,last_name=admin_last_name,email=admin_email,company_id=company.id)
    
    # hashed_password=hash(Member.password)    
    admin_role = get_role_by_name(db, "ADMIN")
    if admin_role:
        assign_role_to_member(db, admin.id, admin_role.id)

    otp = generate_otp()
    redis_client = get_redis_client()
    save_otp(admin_email, otp, redis_client)
    send_actvation_link_email(admin_email, otp)

    db.commit()

    return {
        "message": "Company created and activation OTP sent",
        "company_id": company.id,
        "admin_id": admin.id,
    }


def activate_company_admin(db: Session, email: str, otp: str, password: str):
    member = get_member_by_email(db, email)

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )

    if member.status != StatusEnum.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already active",
        )

    if not verify_otp(email, otp, get_redis_client()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )

    member.password = hash(password)
    member.status = StatusEnum.ACTIVE
    db.commit()
    db.refresh(member)

    return {
        "message": "Account activated successfully",
        "member_id": member.id,
    }

def get_all_company(db:Session):
    return get_all_companies(db)

def all_companies(db: Session,search: str | None = None,domain: str | None = None,subscription: SubscriptionEnum | None = None,sort_by: str = "name",sort_order: str = "desc",):
    return get_compnaies(db=db,search=search,domain=domain,subscription=subscription,sort_by=sort_by,sort_order=sort_order,)

def all_compnaies_asc(db:Session):
    return get_companies_by_asc(db)


def get_company(db: Session, company_id: int):
    company = get_companies_by_id(db, company_id)

    if company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    return company


def delete_company(db: Session, company_id: int):
    id = get_companies_by_id(db, company_id)
 
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")

    delete_company_by_id(db, company_id)
    db.commit()
    return {"message": "Company deleted successfully"}

def edit_company(db: Session,company_id: int,name: str | None = None,domain: str | None = None,logo: str | None = None,subscription: SubscriptionEnum | None = None,):
    company = get_companies_by_id(db, company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found",
        )

    if name is not None and name != company.name:
        existing_company = get_company_by_name(db, name=name)
        if existing_company is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Company name already exists",
            )

    if domain is not None and domain != company.domain:
        existing_domain = get_company_by_domain(db, domain=domain)
        if existing_domain is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Company domain already exists",
            )

    update_company_fields(db=db,company=company,name=name,domain=domain,logo=logo,subscription=subscription,)
    db.commit()
    db.refresh(company)

    return {
        "message": "Company updated successfully",
        "company": company,
    }
