from pydantic import BaseModel, ConfigDict, Field, field_validator

"""
    the fields in category 
    category_id,category_name,description,is_active
    
"""


class CategoryCreate(BaseModel):
    category_name: str = Field(min_length=2, max_length=100)
    description: str | None = None

    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Category name cannot be empty.")

        return value


class CategoryUpdate(BaseModel):
    category_name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None

    @field_validator("category_name")
    @classmethod
    def validate_category_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Category name cannot be empty.")

        return value


class CategoryResponse(BaseModel):
    category_id: int
    category_name: str
    description: str | None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
