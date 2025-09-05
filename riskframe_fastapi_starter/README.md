
# Riskframe FastAPI Starter (Render)

Minimal FastAPI app for Render with a `/health` endpoint and optional Sentry.

## Endpoints
- `/` root hello
- `/health` returns `{ "status": "ok" }`
- `/version` service metadata

## Deploy (Render)
1. Push this folder to a new GitHub repo.
2. In Render: **New +** → **Web Service** → Connect your repo.
3. Environment = **Python**.
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Set `SENTRY_DSN` in Environment (optional).
7. Health check path: `/health`

## Local run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
