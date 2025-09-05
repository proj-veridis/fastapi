# app/main.py
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

APP_VERSION = "0.1.0"
ENV_NAME = os.getenv("ENV", "production")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_DEBUG = os.getenv("SENTRY_DEBUG", "0") == "1"  # optional; set to 1 only for debugging

# --- Sentry (safe init: only if DSN present) ---------------------------------
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENV_NAME,
        traces_sample_rate=0.0,  # perf tracing off for now
        debug=SENTRY_DEBUG,
    )

# --- FastAPI app -------------------------------------------------------------
app = FastAPI(title="Riskframe FastAPI", version=APP_VERSION)

@app.get("/", tags=["meta"])
def root():
    return {"service": "riskframe-api", "message": "Hello from Render", "version": APP_VERSION}

@app.get("/health", tags=["meta"])
def health():
    return JSONResponse({"status": "ok", "ts": int(time.time())})

@app.get("/version", tags=["meta"])
def version():
    return {"version": APP_VERSION, "env": ENV_NAME, "sentry_dsn_loaded": bool(SENTRY_DSN)}

# ---------- Diagnostics / Sentry tests ---------------------------------------

@app.get("/diag", tags=["diag"])
def diag():
    return {
        "env": ENV_NAME,
        "sentry_dsn_loaded": bool(SENTRY_DSN),
        "sentry_debug": SENTRY_DEBUG,
    }

@app.get("/sentry-ping", tags=["diag"])
def sentry_ping():
    sentry_sdk.capture_message("sentry ping from veridis_fastapi")
    return {"sent": True}

@app.get("/sentry-exception", tags=["diag"])
def sentry_exception():
    try:
        1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
    return {"captured": "ZeroDivisionError"}

@app.get("/boom", tags=["diag"])
def boom():
    raise RuntimeError("Test error for Sentry integration")
