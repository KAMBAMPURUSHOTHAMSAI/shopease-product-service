"""Pydantic request and response schemas for Product APIs."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


class ProductWriteBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=100, examples=["Wireless Mouse"])
    description: Optional[str] = Field(
        default=None, max_length=500, examples=["A comfortable wireless mouse"]
    )
    price: float = Field(..., gt=0, allow_inf_nan=False, examples=[799.0])
    stock_quantity: int = Field(..., ge=0, strict=True, examples=[25])
    category: str = Field(..., min_length=1, max_length=50, examples=["Electronics"])
    status: ProductStatus = Field(default=ProductStatus.ACTIVE)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Product name must not be empty or contain only spaces.")
        return cleaned

    @field_validator("description")
    @classmethod
    def clean_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Product category must not be empty or contain only spaces.")
        return cleaned


class ProductCreate(ProductWriteBase):
    """Fields required to create a product."""


class ProductUpdate(ProductWriteBase):
    """Fields accepted by PUT; this endpoint replaces all editable product fields."""


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: str
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category: str
    status: ProductStatus
    created_at: datetime
