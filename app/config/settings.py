"""Application configuration loaded from environment variables or a local .env file."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env when running locally. Docker builds intentionally exclude this file.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    """Small settings object; avoids needing a separate settings package."""

    app_name: str = os.getenv("APP_NAME", "ShopEase Product Service")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    app_description: str = os.getenv(
        "APP_DESCRIPTION",
        "An independent Product Management microservice built with FastAPI.",
    )
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8003"))
    debug: bool = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "yes"}


settings = Settings()
