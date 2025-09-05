# app/main.py
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

# --- Sentry Setup ------------------------------------------------------------
SENTRY_DSN = os.getenv("SENTRY_DSN")
ENV_NAME = os.getenv("ENV", "production")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.0,  # no tracing for now
        environment=ENV_NAME,
    )

# --- FastAPI app -------------------------------------------------------------
app = FastAPI(title="Riskframe FastAPI", version="0.1.0")


@app.get("/", tags=["meta"])
def root():
    """Root hello endpoint."""
    return {
        "service": "riskframe-api",
        "message": "Hello from Render",
        "version": "0.1.0",
    }


@app.get("/health", tags=["meta"])
def health():
    """Simple healthcheck (for UptimeRobot/Render)."""
    return JSONResponse({"status": "ok", "ts": int(time.time())})


@app.get("/version", tags=["meta"])
def version():
    """Show app version and environment."""
    return {"version": "0.1.0", "env": ENV_NAME}


@app.get("/sentry-ping", tags=["meta"])
def sentry_ping():
    """Send a non-crashing message to Sentry."""
    sentry_sdk.capture_message("sentry ping from veridis_fastapi")
    return {"sent": True}


@app.get("/boom", tags=["meta"])
def boom():
    """Force an error to test Sentry integration."""
    raise RuntimeError("Test error for Sentry integration")
