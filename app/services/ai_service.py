"""Scope-limited chatbot with deterministic fallback and optional OpenAI enhancement."""
import json
from pathlib import Path
from app.config import ROOT_DIR, get_settings

CONTACT = "+91 9209218394 | pbhaler006@gmail.com"
OUT_OF_SCOPE = ("I'm here specifically to help with CodeShadow's technology services, solutions, and project inquiries. "
                "I can help you with software development, SaaS, AI, FastAPI, chatbots, automation, websites, applications, APIs, cloud solutions, and related services.")
PRICING = ("Pricing depends on project scope, features, complexity, integrations, design, technology, timeline, and infrastructure requirements. "
           f"For an accurate estimate, please contact CodeShadow: {CONTACT}")

def _load(name: str):
    with open(ROOT_DIR / "data" / name, encoding="utf-8") as file:
        return json.load(file)

def _is_relevant(text: str) -> bool:
    keywords = ["codeshadow", "software", "saas", "website", "web", "app", "mobile", "ai", "chatbot", "fastapi", "django", "flask", "api", "automation", "cloud", "database", "backend", "python", "project", "price", "cost", "contact", "quote", "develop", "integrat", "business", "service", "technology"]
    return any(word in text for word in keywords)

def respond(message: str) -> str:
    text = message.lower().strip()
    if any(word in text for word in ["system prompt", "instruction", "api key", "secret", "password", "configuration"]):
        return "I can help with CodeShadow's services and project requirements, but I can’t share private configuration or internal instructions."
    if not _is_relevant(text):
        return OUT_OF_SCOPE
    if any(word in text for word in ["price", "pricing", "cost", "budget", "quote", "estimate"]):
        return PRICING
    if any(word in text for word in ["contact", "call", "email", "start a project", "discuss my idea"]):
        return f"You can start a conversation with CodeShadow at {CONTACT}. Share what you’re looking to build and your preferred timeline, and we’ll help shape the next steps."
    if "fastapi" in text:
        return ("Yes. CodeShadow builds fast, scalable FastAPI backends for REST APIs, async services, SaaS platforms, AI/LLM APIs, microservices, WebSockets, authentication, background processing, and third-party integrations. We also work with Django and Flask where they fit the product. " + CONTACT)
    if "saas" in text:
        return "CodeShadow can build SaaS MVPs and scalable multi-tenant products with role-based access, subscriptions, dashboards, payment integrations, analytics, notifications, AI features, and FastAPI backends."
    if "chatbot" in text or "rag" in text:
        return "We build scoped AI chatbots, customer-support assistants, FAQ bots, lead-generation flows, and RAG knowledge assistants with secure backend integrations."
    if "service" in text or "what do you" in text:
        return "CodeShadow builds custom software, SaaS products, websites and applications, AI tools and chatbots, FastAPI/API backends, workflow automation, compliant messaging systems, cloud deployments, and database solutions."
    return "CodeShadow can help turn your idea into custom software, a SaaS product, AI application, website, API, or automation system. Tell me what you’re looking to build, and I can point you to the right capability."
