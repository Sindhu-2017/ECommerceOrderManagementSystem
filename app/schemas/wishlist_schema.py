from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.product_schema import ProductResponse


class WishlistResponse(BaseModel):
    wishlist_id: int
    product_id: int
    added_at: datetime
    product: ProductResponse
    model_config = ConfigDict(from_attributes=True)
