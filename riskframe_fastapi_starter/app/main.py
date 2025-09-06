# app/main.py
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

APP_VERSION = "0.1.0"
ENV_NAME = os.getenv("ENV", "production")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_DEBUG = os.getenv("SENTRY_DEBUG", "0") == "1"  # set to 1 temporarily if you need SDK logs

# --- Sentry (safe init; only if DSN provided) --------------------------------
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENV_NAME,
        traces_sample_rate=0.0,   # perf tracing off for now
        debug=SENTRY_DEBUG,       # avoid leaving this on in production
    )

# --- FastAPI app -------------------------------------------------------------
app = FastAPI(title="Riskframe FastAPI", version=APP_VERSION)


@app.get("/", tags=["meta"])
def root():
    """Root hello endpoint to verify service is up."""
    return {"service": "riskframe-api", "message": "Hello from Render", "version": APP_VERSION}


@app.get("/health", tags=["meta"])
def health():
    """Lightweight healthcheck for Render/UptimeRobot."""
    return JSONResponse({"status": "ok", "ts": int(time.time())})


@app.get("/version", tags=["meta"])
def version():
    """Service version and environment details (useful for smoke tests)."""
    return {"version": APP_VERSION, "env": ENV_NAME, "sentry_dsn_loaded": bool(SENTRY_DSN)}


# ---------- Diagnostics / non-crashing Sentry test ---------------------------

@app.get("/diag", tags=["diag"])
def diag():
    """Quick diagnostic snapshot without exposing secrets."""
    return {
        "env": ENV_NAME,
        "sentry_dsn_loaded": bool(SENTRY_DSN),
        "sentry_debug": SENTRY_DEBUG,
    }


@app.get("/sentry-ping", tags=["diag"])
def sentry_ping():
    """Send a harmless message to Sentry to confirm ingestion."""
    sentry_sdk.capture_message("sentry ping from veridis_fastapi")
    return {"sent": True}
