"""REST endpoints for product CRUD operations."""

from typing import Optional

from fastapi import APIRouter, Query, status
from fastapi.responses import Response

from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
)
def create_product(product_data: ProductCreate) -> ProductResponse:
    return product_service.create_product(product_data)


@router.get(
    "/",
    response_model=list[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all products",
)
def get_all_products(
    category: Optional[str] = Query(default=None, description="Filter by exact category name"),
    skip: int = Query(default=0, ge=0, description="Number of products to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Maximum products to return"),
) -> list[ProductResponse]:
    return product_service.get_all_products(category=category, skip=skip, limit=limit)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a product by ID",
)
def get_product_by_id(product_id: str) -> ProductResponse:
    return product_service.get_product_by_id(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a product",
)
def update_product(product_id: str, product_data: ProductUpdate) -> ProductResponse:
    return product_service.update_product(product_id, product_data)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Delete a product",
)
def delete_product(product_id: str) -> Response:
    product_service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
