from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from fastapi.templating import Jinja2Templates
from app.config import ROOT_DIR

router = APIRouter()
templates = Jinja2Templates(directory=str(ROOT_DIR / "templates"))

@router.get("/")
async def home(request: Request): return templates.TemplateResponse(request, "index.html")
@router.get("/privacy")
async def privacy(request: Request): return templates.TemplateResponse(request, "privacy.html")
@router.get("/terms")
async def terms(request: Request): return templates.TemplateResponse(request, "terms.html")
@router.get("/health")
async def health(): return {"status": "ok"}
@router.get("/robots.txt", response_class=PlainTextResponse)
async def robots(): return "User-agent: *\nAllow: /\nSitemap: https://codeshadow.in/sitemap.xml\n"
@router.get("/sitemap.xml")
async def sitemap():
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>https://codeshadow.in{p}</loc></url>' for p in ["/", "/privacy", "/terms"]) + '</urlset>'
    return Response(xml, media_type="application/xml")
