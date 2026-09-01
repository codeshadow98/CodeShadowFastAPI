"""Minimal, authenticated dashboard for project inquiries."""
import hmac
from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import ROOT_DIR, get_settings
from app.database import get_db
from app.models import ProjectInquiry

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory=str(ROOT_DIR / "templates"))


def authenticated(request: Request) -> bool:
    return request.session.get("is_admin") is True


@router.get("/login")
async def login_page(request: Request):
    if authenticated(request):
        return RedirectResponse("/admin/enquiries", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(request, "admin_login.html", {"error": None})


@router.post("/login")
async def login(request: Request, username: str = Form(), password: str = Form()):
    settings = get_settings()
    configured = settings["admin_username"] and settings["admin_password"]
    valid = configured and hmac.compare_digest(username, settings["admin_username"]) and hmac.compare_digest(password, settings["admin_password"])
    if valid:
        request.session.clear()
        request.session["is_admin"] = True
        return RedirectResponse("/admin/enquiries", status_code=status.HTTP_303_SEE_OTHER)
    message = "Admin credentials are not configured." if not configured else "Invalid username or password."
    return templates.TemplateResponse(request, "admin_login.html", {"error": message}, status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/enquiries")
async def enquiries(request: Request, db: Session = Depends(get_db)):
    if not authenticated(request):
        return RedirectResponse("/admin/login", status_code=status.HTTP_303_SEE_OTHER)
    rows = db.scalars(select(ProjectInquiry).order_by(ProjectInquiry.created_at.desc()).limit(250)).all()
    return templates.TemplateResponse(request, "admin_enquiries.html", {"inquiries": rows})
