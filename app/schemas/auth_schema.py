from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username:str =Field(min_length=3,max_length=50)
    email:EmailStr
    password:str =Field(min_length=6,max_length=20)
    first_name:str=Field(min_length=1,max_length=50)
    last_name:str=Field(min_length=1,max_length=50)
    phone :str = Field(pattern=r"^[0-9]{10}$")
    date_of_birth: date

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

class CustomerProfileResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str
    date_of_birth: date
    model_config = ConfigDict(from_attributes=True)


class UserProfileResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    customer: CustomerProfileResponse | None = None
    model_config = ConfigDict(from_attributes=True)



