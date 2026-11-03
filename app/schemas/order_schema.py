from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

# Order item schemas
class OrderItemCreate(BaseModel):
    product_id:int =Field(gt=0)
    quantity:int=Field(gt=0)

class OrderItemResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    order_item_id:int
    product_id:int
    quantity:int
    unit_price:Decimal
    subtotal:Decimal

# Order schemas
class OrderCreate(BaseModel):
    shipping_id:int = Field(gt=0)
    items:list[OrderItemCreate]=Field(min_length=1)

class OrderResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    order_id:int
    customer_id:int
    shipping_id:int
    order_date:datetime
    total_amount:Decimal
    order_status:str

    shipping_recipient_name:str
    shipping_phone:str
    shipping_address_line:str
    shipping_city:str
    shipping_state:str
    shipping_pincode:str

    items:list[OrderItemResponse]
     