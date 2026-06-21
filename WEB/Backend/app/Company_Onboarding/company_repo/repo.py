from sqlalchemy.orm import Session

from ..company_model.company_model import Company,SubscriptionEnum
from ...Authentication_Flow.authentication_model.member_model import Member 
from ...Authentication_Flow.authentication_model.member_model import MemberRoleMapping
from ...Authentication_Flow.authentication_model.role_model import Role
from sqlalchemy import asc , desc

def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()

def get_member_by_email(db: Session, email: str):
    return db.query(Member).filter(Member.email == email).first()

def get_company_by_domain(db:Session,domain:str):
    return db.query(Company).filter(Company.domain==domain).first()

def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def get_companies_by_desc(db: Session):
    return db.query(Company).order_by(Company.id.desc()).all()

def get_companies_by_asc(db: Session):
    return db.query(Company).order_by(Company.id.asc()).all()

def get_all_companies(db:Session):
    return db.query(Company).all()

def get_compnaies(db:Session,search:str |None=None,domain:str |None=None,subscription: SubscriptionEnum | None = None,sort_by:str="name",sort_order:str="desc",):
    query=db.query(Company)
    if search:
        search_by=search.strip()
        query=query.filter((Company.name.ilike(search_by)) | (Company.domain.ilike(search_by)))
        if domain:
            query=query.filter(Company.domain==domain)
        if subscription:
            query=query.filter(Company.subcription == subscription)

        sorting={'name':Company.name,
                 'domain':Company.domain,}
        sortin=sorting.get(sort_by,Company.name)
        if sort_order.lower() =="asc":
            query=query.order_by(asc(sortin))
        else:
            query=query.order_by(desc(sortin))

        return query.all()
    
def get_companies_by_id(db: Session,company_id:int):
    
    return db.query(Company).filter(Company.id==company_id).first()

def create_company(db: Session, name: str, domain:str, logo:str,subscription:SubscriptionEnum):  #logo: str
    company = Company(
        name=name,
        logo=logo,
        domain=domain,
        subcription=subscription,
    )
    db.add(company)
    db.flush()
    return company


def create_company_admin(db: Session, first_name: str,last_name:str, email: str, company_id: int):
    member = Member(
        first_name=first_name,
        last_name=last_name,
        email=email,
        status="PENDING",
        password=None,
        company_id=company_id,
    )

    db.add(member)
    db.flush()
    return member

def update_company_fields(db: Session,company: Company,name: str | None = None,domain: str | None = None,logo: str | None = None,subscription: SubscriptionEnum | None = None,):
    if name is not None:
        company.name = name

    if domain is not None:
        company.domain = domain

    if logo is not None:
        company.logo = logo

    if subscription is not None:
        company.subcription = subscription

    db.flush()
    return company


def assign_role_to_member(db: Session, member_id: int, role_id: int):
    mapping = MemberRoleMapping(member_id=member_id, role_id=role_id)
    db.add(mapping)
    db.flush()
    return mapping


def delete_company_by_id(db: Session, company_id: int):
    company_remove=  db.query(Company).filter(Company.id==company_id).first()
    if company_remove:
        db.delete(company_remove)
        db.flush()
    
    return company_remove


