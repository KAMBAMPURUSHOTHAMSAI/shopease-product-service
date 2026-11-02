"""Product domain model used by the in-memory service layer."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    product_id: str
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category: str
    status: str
    created_at: datetime
