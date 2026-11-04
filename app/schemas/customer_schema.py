from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class CustomerUserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CustomerAdminResponse(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    phone: str
    date_of_birth: date
    user: CustomerUserResponse
    model_config = ConfigDict(from_attributes=True)