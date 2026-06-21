from pydantic import BaseModel ,EmailStr ,Field

class Request(BaseModel):
    email:EmailStr

class Verify(BaseModel):
    email:EmailStr
    otp:str


class Token(BaseModel):
    access_token:str
    token_type:str
   

class TokenData(BaseModel):
    id:int
    


class MemberLogin(BaseModel):
    email:EmailStr
    password:str=Field(min_length=6)