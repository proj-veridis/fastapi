
import os
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sentry_sdk

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=0.0)  # no tracing by default

app = FastAPI(title="Riskframe FastAPI", version="0.1.0")

@app.get("/", tags=["meta"])
def root():
    return {"service": "riskframe-api", "message": "Hello from Render", "version": "0.1.0"}

@app.get("/health", tags=["meta"])
def health():
    # Simple, fast healthcheck
    return JSONResponse({"status": "ok", "ts": int(time.time())})

@app.get("/version", tags=["meta"])
def version():
    return {"version": "0.1.0", "env": os.getenv("ENV", "production")}
