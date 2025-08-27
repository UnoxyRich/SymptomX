
from __future__ import annotations
from typing import List, Tuple
from . import triage

KEYWORDS = {
    "fever": {
        "name": "Viral Fever",
        "meds": [("Paracetamol", "500 mg every 6–8h (max 3g/day)", "https://en.wikipedia.org/wiki/Paracetamol")],
        "triage": "routine",
        "advice": "Hydrate and rest. Seek care if fever > 39.5°C or lasts > 3 days."
    },
    "headache": {
        "name": "Tension Headache",
        "meds": [("Ibuprofen", "200–400 mg every 6–8h with food", "https://en.wikipedia.org/wiki/Ibuprofen")],
        "triage": "routine",
        "advice": "Limit screen time, hydrate, consider gentle neck stretches."
    },
    "diarrhea": {
        "name": "Acute Gastroenteritis",
        "meds": [("Oral Rehydration Salts", "Sip small amounts frequently", "https://en.wikipedia.org/wiki/Oral_rehydration_therapy")],
        "triage": "routine",
        "advice": "Use ORS, avoid dairy/spicy foods. Seek care if blood in stool or dehydration."
    },
    "chest pain": {
        "name": "Possible Cardiac Pain",
        "meds": [],
        "triage": "emergency",
        "advice": "Call emergency services immediately, especially if pain radiates to arm/jaw or with shortness of breath."
    },
    "cough": {
        "name": "Upper Respiratory Infection",
        "meds": [("Dextromethorphan", "10–20 mg every 4h as needed", "https://en.wikipedia.org/wiki/Dextromethorphan")],
        "triage": "routine",
        "advice": "Honey/tea may help. Seek care if cough > 3 weeks, fever, or breathing difficulty."
    },
}

def _match_score(symptoms: str, key: str) -> float:
    text = symptoms.lower()
    return 1.0 if key in text else (0.6 if any(w in text for w in key.split()) else 0.0)

def score(symptoms: str):
    candidates = []
    for k, v in KEYWORDS.items():
        sc = _match_score(symptoms, k)
        if sc > 0.0:
            candidates.append((sc, v))
    if not candidates:
        # Default catch-all
        return {
            "top": {
                "name": "Non-specific symptoms",
                "confidence": 0.3,
                "triage": "routine",
                "medications": [{"name": "Rest/Fluids", "dosage": "As tolerated", "info_url": "https://en.wikipedia.org/wiki/Fluid_replacement"}],
            },
            "others": [],
            "advice": "Monitor symptoms. If they worsen or persist, seek medical attention."
        }
    candidates.sort(key=lambda x: x[0], reverse=True)
    top_sc, top_item = candidates[0]
    others = candidates[1:3]
    return {
        "top": {
            "name": top_item["name"],
            "confidence": round(min(1.0, 0.5 + 0.5*top_sc), 2),
            "triage": top_item["triage"],
            "medications": [{"name": m[0], "dosage": m[1], "info_url": m[2]} for m in top_item["meds"]],
        },
        "others": [{
            "name": it["name"],
            "confidence": round(0.4 * sc, 2),
            "triage": it["triage"],
            "medications": [{"name": m[0], "dosage": m[1], "info_url": m[2]} for m in it["meds"]],
        } for sc, it in others],
        "advice": top_item["advice"],
    }

def triage_message(level: str) -> str:
    if level == "emergency":
        return "⚠️ This may require urgent care. Seek emergency services immediately."
    if level == "urgent":
        return "Please see a clinician soon (within 24–48 hours)."
    return "This seems non-urgent. Monitor and use self-care."

def chat_reply(text: str) -> str:
    s = text.lower()
    if "fever" in s:
        return "For fever, stay hydrated and consider paracetamol (500 mg). Seek care if high/lasting fever."
    if "headache" in s:
        return "For headache, rest and try ibuprofen (200–400 mg) with food unless contraindicated."
    if "diarrhea" in s:
        return "Use oral rehydration salts (ORS). Seek care if blood in stool or signs of dehydration."
    if "chest" in s and "pain" in s:
        return "Chest pain can be serious — seek emergency care immediately."
    return "Tell me your main symptoms, when they started, and anything that makes them better or worse."
