from pydantic import BaseModel, Field
from typing import Literal

class ContactRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    phone: str = Field(min_length=7, max_length=30)
    company: str | None = Field(default=None, max_length=120)
    project_type: Literal["Website", "Web Application", "Mobile Application", "SaaS", "AI Application", "AI Chatbot", "AI Tool", "Automation", "FastAPI / Backend", "API Integration", "Bulk Messaging", "Cloud / DevOps", "Other"]
    description: str = Field(min_length=15, max_length=4000)
    budget: str | None = Field(default=None, max_length=80)
    timeline: str | None = Field(default=None, max_length=80)

class ContactResponse(BaseModel):
    message: str
