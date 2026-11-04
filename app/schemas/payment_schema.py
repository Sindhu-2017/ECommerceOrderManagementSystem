from pydantic import BaseModel, ConfigDict


class PaymentVerify(BaseModel):
    razorpay_payment_id: str
    razorpay_payment_link_id: str
    razorpay_payment_link_reference_id: str
    razorpay_payment_link_status: str
    razorpay_signature: str

class PaymentResponse(BaseModel):
    payment_id:int
    order_id:int
    payment_method:str
    payment_amount:float
    payment_status:str
    razorpay_payment_link_id: str
    payment_link_url: str
    transaction_id:str|None
    model_config=ConfigDict(from_attributes=True)