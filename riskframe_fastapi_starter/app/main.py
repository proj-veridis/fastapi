# app/main.py
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

# --- Sentry (optional) -------------------------------------------------------
# If SENTRY_DSN is set in Render → Environment, errors will be sent to Sentry.
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    # Keep tracing disabled for now to reduce noise/cost.
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.0)

# --- FastAPI app -------------------------------------------------------------
app = FastAPI(title="Riskframe FastAPI", version="0.1.0")


@app.get("/", tags=["meta"])
def root():
    """Simple hello endpoint to verify the app is running."""
    return {
        "service": "riskframe-api",
        "message": "Hello from Render",
        "version": "0.1.0",
    }


@app.get("/health", tags=["meta"])
def health():
    """Fast healthcheck for Render/UptimeRobot."""
    return JSONResponse({"status": "ok", "ts": int(time.time())})


@app.get("/version", tags=["meta"])
def version():
    """Return app version and environment name (if set)."""
    return {"version": "0.1.0", "env": os.getenv("ENV", "production")}


@app.get("/boom", tags=["meta"])
def boom():
    """Intentional error to verify Sentry integration. Remove after testing."""
    raise RuntimeError("Test error for Sentry integration")
