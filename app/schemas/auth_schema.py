from datetime import date

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username:str =Field(min_length=3,max_length=50)
    email:EmailStr
    password:str =Field(min_length=6,max_length=20)
    first_name:str=Field(min_length=1,max_length=50)
    last_name:str=Field(min_length=1,max_length=50)
    phone :str = Field(min_length=10,max_length=15)
    date_of_birth: date

class LoginRequest(BaseModel):
    username:str
    password:str

class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str ="bearer"

class RefreshRequest(BaseModel):
    refresh_token:str =Field(min_length=20,max_length=4096)

class LogoutRequest(BaseModel):
    refresh_token:str =Field(min_length=20,max_length=4096)

class MessageResponse(BaseModel):
    message:str


