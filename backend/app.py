
from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .routers import diagnosis, chat

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="SymptomX")

# Mount static assets
app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIR / "assets")), name="assets")

# Routers
app.include_router(diagnosis.router)
app.include_router(chat.router)

# Serve index.html
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

# Health
@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"ok": True}


# Serve about.html
@app.get("/about.html", include_in_schema=False)
def about():
    return FileResponse(str(FRONTEND_DIR / "about.html"))
