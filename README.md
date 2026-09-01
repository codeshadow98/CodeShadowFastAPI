# CodeShadow

Premium FastAPI-powered technology services website for CodeShadow. It includes responsive service discovery, a conversion-focused inquiry form, SEO routes, legal pages, and a scope-limited CodeShadow AI Assistant.

## Stack

- FastAPI, Jinja2, Pydantic
- Vanilla HTML, CSS, and JavaScript
- Optional OpenAI integration configuration (the deterministic knowledge-base assistant works without an API key)

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. API documentation is at `/docs`; health check is at `/health`.

Copy `.env.example` to `.env` and set only values required for your deployment. Never commit `.env`.

## Database and inquiry storage

Every valid `POST /api/contact` submission is stored in the `project_inquiries` table. Local development defaults to `codeshadow.db` (SQLite) so the application runs without extra setup. This local database is ignored by Git.

For production, set `DATABASE_URL` to a PostgreSQL connection string. Standard URLs beginning with `postgresql://` are supported and use the included `psycopg` driver. Apply migrations before deploying a schema change:

```bash
alembic upgrade head
```

On FastAPI Cloud, connect a PostgreSQL provider through the **Integrations** tab (for example, Neon or Supabase), or add `DATABASE_URL` through Environment Variables and mark it as a secret. FastAPI Cloud integrations create this environment variable as an encrypted secret. Run `alembic upgrade head` against the managed database as part of the release process; do not rely on automatic production schema creation. The app entry point is configured in `pyproject.toml`, so the current deployment command is:

```bash
fastapi deploy
```

## Enquiries dashboard

The authenticated dashboard is at `/admin/login`. Copy `.env.example` to `.env`, set a long, unique `SECRET_KEY`, `ADMIN_USERNAME`, and `ADMIN_PASSWORD`, and restart the app. On FastAPI Cloud, configure all three as encrypted secrets in Environment Variables. The dashboard shows the latest 250 saved inquiries and has a sign-out action.

## Endpoints

- `GET /` — main website
- `GET /health` — service health
- `POST /api/chat` — CodeShadow-only assistant
- `POST /api/contact` — validated inquiry intake
- `GET /robots.txt`, `GET /sitemap.xml`

## Knowledge base

Update `app/data/company.json`, `services.json`, `technologies.json`, and `faq.json` as offerings evolve. The chatbot enforces scope, pricing guidance, contact details, and private-information protection in `app/services/ai_service.py`.

## Production notes

Use `uvicorn app.main:app` as the ASGI entry point. Configure production environment variables in the deployment provider, use HTTPS, and connect `codeshadow.in` through the provider’s current custom-domain workflow. Verify the current [FastAPI Cloud documentation](https://fastapicloud.com/) before deployment, as provider commands and DNS values can change.

## GitHub

```bash
git init
git add .
git commit -m "Initial CodeShadow website"
git branch -M main
git remote add origin <GITHUB_REPOSITORY>
git push -u origin main
```
