from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

'''
the product table contains
product_id,category_id,product_name,description,price,stock_quantity,image_path,is_active
'''

class ProductCreate(BaseModel):
    category_id:int = Field(gt=0)
    product_name :str = Field(
        min_length=2,
        max_length=50
    )
    description:str|None =None
    price :Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    stock_quantity:int = Field(ge=0)

class ProductUpdate(BaseModel):
    category_id:int|None =Field(default=None,gt=0)
    product_name :str |None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    description:str|None =None
    price :Decimal |None= Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    stock_quantity:int |None = Field(default=None,ge=0)

class ProductResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    product_id:int
    category_id:int
    product_name:str
    description:str|None
    price:Decimal
    stock_quantity:int
    image_path:str|None
    is_active:bool
