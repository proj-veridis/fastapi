# app/main.py
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

APP_VERSION = "0.1.0"
ENV_NAME = os.getenv("ENV", "production")
SENTRY_DSN = os.getenv("SENTRY_DSN")
SENTRY_DEBUG = os.getenv("SENTRY_DEBUG", "0") == "1"  # turn on to see SDK logs in Render

if SENTRY_DSN:
    # Enable debug only while diagnosing; turn off after it works.
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENV_NAME,
        traces_sample_rate=0.0,
        debug=SENTRY_DEBUG,
    )

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


# --- Diagnostics & Sentry tests ----------------------------------------------

@app.get("/diag", tags=["diag"])
def diag():
    # helps confirm what the server actually sees
    return {
        "env": ENV_NAME,
        "sentry_dsn_loaded": bool(SENTRY_DSN),
        "sentry_debug": SENTRY_DEBUG,
        "tips": "If sentry_dsn_loaded=false, check Render → Environment → SENTRY_DSN.",
    }


@app.get("/sentry-ping", tags=["diag"])
def sentry_ping():
    # non-crashing message
    sentry_sdk.capture_message("sentry ping from veridis_fastapi")
    return {"sent": True}


@app.get("/sentry-exception", tags=["diag"])
def sentry_exception():
    # capture an exception without crashing the request
    try:
        1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
    return {"captured": "ZeroDivisionError"}


@app.get("/boom", tags=["diag"])
def boom():
    # crashing error (500) — use once to verify, then remove
    raise RuntimeError("Test error for Sentry integration")
