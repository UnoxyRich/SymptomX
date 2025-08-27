
from __future__ import annotations
from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    GEMINI_API_KEY: str | None = Field(default=None)

    class Config:
        env_file = ROOT / ".env"
        extra = "ignore"

def _load_json_key() -> dict:
    cfg_path = ROOT / "gemini.json"
    if cfg_path.exists():
        try:
            data = json.loads(cfg_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return {"GEMINI_API_KEY": data.get("api_key") or data.get("GEMINI_API_KEY")}
        except Exception:
            pass
    return {}

settings = Settings(**_load_json_key())
