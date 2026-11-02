"""Application entry point for the ShopEase Product Service."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.config.settings import settings
from app.routers.product_routes import router as product_router
from app.services.product_service import (
    DuplicateProductIDError,
    InvalidProductIDError,
    ProductNotFoundError,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shopease-product-service")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    debug=settings.debug,
)
app.include_router(product_router)


@app.get("/", tags=["Health"], summary="Service information")
def root() -> dict[str, str]:
    return {"service": settings.app_name, "status": "running"}


@app.get("/health", tags=["Health"], summary="Health check")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "ShopEase Product Service"}


@app.exception_handler(InvalidProductIDError)
async def invalid_product_id_handler(
    request: Request, exc: InvalidProductIDError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(
    request: Request, exc: ProductNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicateProductIDError)
async def duplicate_product_id_handler(
    request: Request, exc: DuplicateProductIDError
) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(RequestValidationError)
async def request_validation_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation failed.",
            "errors": jsonable_encoder(exc.errors()),
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unexpected error while processing %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected internal server error occurred."},
    )
