
from __future__ import annotations
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class Medication(BaseModel):
    name: str
    dosage: str
    info_url: Optional[str] = None

class Possibility(BaseModel):
    name: str
    confidence: float = Field(ge=0, le=1)
    triage: Literal["emergency", "urgent", "routine"] = "routine"
    medications: List[Medication] = []

class DiagnoseRequest(BaseModel):
    symptoms: str

class DiagnoseResponse(BaseModel):
    top: Possibility
    others: List[Possibility]
    advice: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
