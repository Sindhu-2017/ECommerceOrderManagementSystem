from datetime import datetime
from pydantic import BaseModel,Field,ConfigDict
'''
shipping table contains
    recipient_name
    phone
    address_line
    city
    state
    pincode
    is_default
    created_at
'''
    


class ShippingCreate(BaseModel):
    recipient_name:str = Field(min_length =1,max_length=100)
    phone :str = Field(pattern=r"^[0-9]{10}$")
    address_line:str=Field(min_length=1,max_length=200)
    city:str=Field(min_length=1,max_length=100)
    state:str=Field(min_length=1,max_length=100)
    pincode:str=Field(pattern=r"^[0-9]{6}$")
    is_default:bool=False

class ShippingUpdate(BaseModel):
    recipient_name:str |None = Field(default=None,min_length =1,max_length=100)
    phone :str  |None = Field(default=None,pattern=r"^[0-9]{10}$")
    address_line:str |None =Field(default=None,min_length=1,max_length=200)
    city:str |None =Field(default=None,min_length=1,max_length=100)
    state:str |None =Field(default=None,min_length=1,max_length=100)
    pincode:str |None =Field(default=None,pattern=r"^[0-9]{6}$")
    is_default:bool |None =None

class ShippingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    shipping_id: int
    customer_id: int
    recipient_name: str
    phone: str
    address_line: str
    city: str
    state: str
    pincode: str
    is_default: bool
    created_at: datetime


