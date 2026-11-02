"""Business logic and in-memory storage for products."""

from datetime import datetime, timezone
from uuid import uuid4
from typing import Optional

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductNotFoundError(Exception):
    """Raised when a requested product does not exist."""


class InvalidProductIDError(Exception):
    """Raised when a product ID is not a valid UUID string."""


class DuplicateProductIDError(Exception):
    """Raised if a generated product ID is already present."""


# This dictionary is intentionally in-memory for this training task.
# All data is lost when the Python process or container is restarted.
_products: dict[str, Product] = {}


def _normalize_product_id(product_id: str) -> str:
    from uuid import UUID

    try:
        return str(UUID(product_id))
    except (ValueError, TypeError, AttributeError) as exc:
        raise InvalidProductIDError("Product ID must be a valid UUID.") from exc


def create_product(product_data: ProductCreate) -> Product:
    product_id = str(uuid4())
    if product_id in _products:
        raise DuplicateProductIDError("A product with this ID already exists.")

    product = Product(
        product_id=product_id,
        created_at=datetime.now(timezone.utc),
        **product_data.model_dump(),
    )
    _products[product_id] = product
    return product


def get_all_products(
    category: Optional[str] = None, skip: int = 0, limit: int = 10
) -> list[Product]:
    products = list(_products.values())
    if category:
        requested_category = category.strip().casefold()
        products = [
            product for product in products
            if product.category.casefold() == requested_category
        ]
    return products[skip : skip + limit]


def get_product_by_id(product_id: str) -> Product:
    normalized_id = _normalize_product_id(product_id)
    product = _products.get(normalized_id)
    if product is None:
        raise ProductNotFoundError(f"Product with ID '{normalized_id}' was not found.")
    return product


def update_product(product_id: str, product_data: ProductUpdate) -> Product:
    normalized_id = _normalize_product_id(product_id)
    existing_product = _products.get(normalized_id)
    if existing_product is None:
        raise ProductNotFoundError(f"Product with ID '{normalized_id}' was not found.")

    updated_fields = product_data.model_dump()
    updated_product = Product(
        product_id=existing_product.product_id,
        created_at=existing_product.created_at,
        **updated_fields,
    )
    _products[normalized_id] = updated_product
    return updated_product


def delete_product(product_id: str) -> None:
    normalized_id = _normalize_product_id(product_id)
    if normalized_id not in _products:
        raise ProductNotFoundError(f"Product with ID '{normalized_id}' was not found.")
    del _products[normalized_id]
