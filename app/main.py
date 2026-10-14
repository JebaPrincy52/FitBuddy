"""FitBuddy FastAPI entry point."""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI(title="FitBuddy - AI Fitness Plan Generator", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.on_event("startup")
def startup() -> None:
    init_db()
