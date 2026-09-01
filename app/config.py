from functools import lru_cache
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent
load_dotenv(ROOT_DIR.parent / ".env")

@lru_cache
def get_settings():
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "site_url": "https://codeshadow.in",
        "secret_key": os.getenv("SECRET_KEY", "development-only-change-before-production"),
        "admin_username": os.getenv("ADMIN_USERNAME", ""),
        "admin_password": os.getenv("ADMIN_PASSWORD", ""),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
