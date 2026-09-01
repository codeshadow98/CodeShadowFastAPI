from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from app.config import ROOT_DIR
from app.config import get_settings
from app.database import Base, DATABASE_URL, engine
from app import models  # noqa: F401 - register ORM models
from app.routes import pages, chat, contact, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # SQLite makes local first-run easy. Production PostgreSQL schema changes are
    # applied through Alembic before deployment, not automatically at startup.
    if DATABASE_URL.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="CodeShadow", version="1.0.0", docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)
settings = get_settings()
app.add_middleware(SessionMiddleware, secret_key=settings["secret_key"], https_only=settings["environment"] == "production", same_site="lax")
app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "static")), name="static")
app.include_router(pages.router)
app.include_router(chat.router)
app.include_router(contact.router)
app.include_router(admin.router)
