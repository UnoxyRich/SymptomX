
from __future__ import annotations
from typing import List, Tuple
from . import triage

# Keyword-to-condition map. Each key is a simple keyword trigger checked against the user's symptom text.
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
    "cold": {
        "name": "Common Cold (Viral URI)",
        "meds": [
            ("Paracetamol", "500 mg every 6–8h for fever/pain (max 3g/day)", "https://en.wikipedia.org/wiki/Paracetamol"),
            ("Ibuprofen", "200–400 mg every 6–8h with food for aches", "https://en.wikipedia.org/wiki/Ibuprofen"),
            ("Dextromethorphan", "10–20 mg every 4h as needed for cough", "https://en.wikipedia.org/wiki/Dextromethorphan")
        ],
        "triage": "routine",
        "advice": "Rest, fluids. Honey (not for <1 yr) may help cough. Seek care for shortness of breath or fever > 3 days."
    },
    "sore throat": {
        "name": "Pharyngitis (Sore Throat)",
        "meds": [
            ("Paracetamol", "500 mg every 6–8h for pain", "https://en.wikipedia.org/wiki/Paracetamol"),
            ("Ibuprofen", "200–400 mg every 6–8h with food for pain", "https://en.wikipedia.org/wiki/Ibuprofen"),
            ("Salt-water gargle", "1/2 tsp salt in warm water, gargle 2–3×/day", "https://en.wikipedia.org/wiki/Gargling")
        ],
        "triage": "routine",
        "advice": "Hydrate, avoid irritants. Seek care if lasting > 1 week, drooling/dysphagia, or rash + high fever."
    },
    "flu": {
        "name": "Influenza (Flu)",
        "meds": [
            ("Paracetamol", "500 mg every 6–8h for fever", "https://en.wikipedia.org/wiki/Paracetamol"),
            ("Ibuprofen", "200–400 mg every 6–8h for aches", "https://en.wikipedia.org/wiki/Ibuprofen")
        ],
        "triage": "routine",
        "advice": "Rest, fluids. Urgent care if chest pain, trouble breathing, confusion, or dehydration."
    },
    "sinus": {
        "name": "Acute Rhinosinusitis",
        "meds": [
            ("Saline nasal rinse", "Use daily as needed", "https://en.wikipedia.org/wiki/Nasal_irrigation"),
            ("Ibuprofen", "200–400 mg every 6–8h for facial pain", "https://en.wikipedia.org/wiki/Ibuprofen")
        ],
        "triage": "routine",
        "advice": "Humidify, warm compress. Seek care if swelling around eyes, severe headache, or >10 days with high fever."
    },
    "allergy": {
        "name": "Allergic Rhinitis (Hay Fever)",
        "meds": [
            ("Loratadine", "10 mg once daily", "https://en.wikipedia.org/wiki/Loratadine"),
            ("Cetirizine", "10 mg once daily", "https://en.wikipedia.org/wiki/Cetirizine"),
            ("Saline nasal spray", "Use as needed", "https://en.wikipedia.org/wiki/Saline_(medicine)")
        ],
        "triage": "routine",
        "advice": "Avoid triggers (dust/pollen), rinse after outdoor exposure. Seek care for wheeze or severe swelling."
    },
    "ear pain": {
        "name": "Earache (Non-specific)",
        "meds": [
            ("Paracetamol", "500 mg every 6–8h for pain", "https://en.wikipedia.org/wiki/Paracetamol"),
            ("Ibuprofen", "200–400 mg every 6–8h with food", "https://en.wikipedia.org/wiki/Ibuprofen")
        ],
        "triage": "routine",
        "advice": "Keep ear dry, avoid inserting objects. Seek care for fever, drainage with severe pain, or hearing loss."
    },
    "pink eye": {
        "name": "Conjunctivitis (Pink Eye)",
        "meds": [
            ("Artificial tears", "1–2 drops as needed", "https://en.wikipedia.org/wiki/Artificial_tears"),
            ("Warm compress", "5–10 min, 3–4×/day", "https://en.wikipedia.org/wiki/Conjunctivitis")
        ],
        "triage": "routine",
        "advice": "Hand hygiene, avoid touching eyes. Urgent care if eye pain, light sensitivity, or vision changes."
    },
    "stye": {
        "name": "Hordeolum (Stye)",
        "meds": [
            ("Warm compress", "10–15 min, 3–4×/day", "https://en.wikipedia.org/wiki/Stye"),
            ("Paracetamol", "500 mg every 6–8h for tenderness", "https://en.wikipedia.org/wiki/Paracetamol")
        ],
        "triage": "routine",
        "advice": "Do not squeeze. Seek care if spreading redness, fever, or no improvement in 1 week."
    },
    "nausea vomiting": {
        "name": "Nausea/Vomiting (Gastroenteritis likely)",
        "meds": [
            ("Oral Rehydration Solution (ORS)", "Small frequent sips", "https://en.wikipedia.org/wiki/Oral_rehydration_therapy"),
            ("Bismuth subsalicylate", "As on label (if not contraindicated)", "https://en.wikipedia.org/wiki/Bismuth_subsalicylate")
        ],
        "triage": "routine",
        "advice": "Clear liquids → bland foods. Care if blood in vomit, severe dehydration, or RLQ abdominal pain."
    },
    "constipation": {
        "name": "Constipation",
        "meds": [
            ("Fiber (psyllium)", "As on label with plenty of water", "https://en.wikipedia.org/wiki/Psyllium"),
            ("Polyethylene glycol (PEG)", "As on label", "https://en.wikipedia.org/wiki/Polyethylene_glycol#Medical_uses")
        ],
        "triage": "routine",
        "advice": "Increase fluids, fiber, activity. Care if severe abdominal pain, vomiting, or blood in stool."
    },
    "acid reflux": {
        "name": "Indigestion / GERD",
        "meds": [
            ("Antacid", "As needed after meals", "https://en.wikipedia.org/wiki/Antacid"),
            ("Omeprazole", "20 mg once daily short-term", "https://en.wikipedia.org/wiki/Omeprazole")
        ],
        "triage": "routine",
        "advice": "Smaller meals, avoid spicy/greasy foods, elevate head when sleeping. Care for black stools or weight loss."
    },
    "uti": {
        "name": "Urinary Tract Infection (suspected)",
        "meds": [
            ("Fluids", "Drink extra water", "https://en.wikipedia.org/wiki/Urinary_tract_infection"),
            ("Paracetamol", "500 mg every 6–8h for discomfort", "https://en.wikipedia.org/wiki/Paracetamol")
        ],
        "triage": "routine",
        "advice": "Burning/frequency suggests UTI—seek testing for antibiotics. Urgent if fever/flank pain (possible kidney infection)."
    },
    "menstrual cramps": {
        "name": "Dysmenorrhea (Menstrual Cramps)",
        "meds": [
            ("Ibuprofen", "200–400 mg every 6–8h with food", "https://en.wikipedia.org/wiki/Ibuprofen"),
            ("Heat pad", "Apply to lower abdomen as needed", "https://en.wikipedia.org/wiki/Heat_therapy")
        ],
        "triage": "routine",
        "advice": "Light activity and heat help. Care if unusually severe, prolonged bleeding, or pregnancy possible."
    },
    "back pain": {
        "name": "Low Back Strain (Non-specific)",
        "meds": [
            ("Paracetamol", "500 mg every 6–8h for pain", "https://en.wikipedia.org/wiki/Paracetamol"),
            ("Ibuprofen", "200–400 mg every 6–8h with food", "https://en.wikipedia.org/wiki/Ibuprofen")
        ],
        "triage": "routine",
        "advice": "Gentle movement, avoid heavy lifting. Urgent care if numbness/weakness, incontinence, or trauma."
    },
    "ankle sprain": {
        "name": "Ankle Sprain",
        "meds": [
            ("Rest/Ice/Compression/Elevation (RICE)", "First 48 hours", "https://en.wikipedia.org/wiki/RICE_(medicine)"),
            ("Ibuprofen", "200–400 mg every 6–8h with food for pain/swelling", "https://en.wikipedia.org/wiki/Ibuprofen")
        ],
        "triage": "routine",
        "advice": "Protect joint; gradual return to activity. Care if you cannot bear weight or visible deformity."
    },
    "migraine": {
        "name": "Migraine",
        "meds": [
            ("Ibuprofen", "400 mg at onset (per label)", "https://en.wikipedia.org/wiki/Ibuprofen"),
            ("Paracetamol", "500–1000 mg at onset", "https://en.wikipedia.org/wiki/Paracetamol")
        ],
        "triage": "routine",
        "advice": "Dark, quiet room; hydration. Urgent care if worst-ever headache, neuro deficits, head injury, or fever + stiff neck."
    },
    "dermatitis": {
        "name": "Dermatitis / Eczema (Mild)",
        "meds": [
            ("Moisturizer (emollient)", "Apply 2–3×/day", "https://en.wikipedia.org/wiki/Emollient"),
            ("Hydrocortisone 1% cream", "Thin layer 1–2×/day for a few days", "https://en.wikipedia.org/wiki/Hydrocortisone")
        ],
        "triage": "routine",
        "advice": "Avoid irritants/harsh soaps; short lukewarm showers. Care if infection (pus, spreading redness, fever)."
    },
    "acne": {
        "name": "Acne (Mild)",
        "meds": [
            ("Benzoyl peroxide 2.5–5%", "Apply daily (avoid eyes)", "https://en.wikipedia.org/wiki/Benzoyl_peroxide"),
            ("Adapalene 0.1% gel", "Apply nightly if tolerated", "https://en.wikipedia.org/wiki/Adapalene")
        ],
        "triage": "routine",
        "advice": "Gentle cleanser, avoid picking. Care for scarring cystic acne."
    },
    "insect bite": {
        "name": "Insect Bite / Sting (Mild)",
        "meds": [
            ("Cold pack", "10–15 min intervals", "https://en.wikipedia.org/wiki/Cold_compress"),
            ("Loratadine", "10 mg once daily for itch", "https://en.wikipedia.org/wiki/Loratadine"),
            ("Hydrocortisone 1% cream", "Thin layer 1–2×/day for itch", "https://en.wikipedia.org/wiki/Hydrocortisone")
        ],
        "triage": "routine",
        "advice": "Wash with soap/water. EMERGENCY if trouble breathing, face/tongue swelling, or widespread hives."
    },
    "minor burn": {
        "name": "Minor Burn (First-degree)",
        "meds": [
            ("Cool running water", "10–20 minutes immediately", "https://en.wikipedia.org/wiki/Burn#First_aid"),
            ("Paracetamol", "500 mg every 6–8h for pain", "https://en.wikipedia.org/wiki/Paracetamol")
        ],
        "triage": "routine",
        "advice": "Do not apply ice or butter. Cover with clean non-stick dressing. Care for large blisters or burns to face/genitals."
    }
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

# Back-compat (routers should import from providers.triage)
def triage_message(level: str) -> str:
    if (level or "").lower().strip() == "emergency":
        return "⚠️ This may require urgent care. Seek emergency services immediately."
    if (level or "").lower().strip() == "urgent":
        return "Please see a clinician soon (within 24–48 hours)."
    return "This seems non-urgent. Monitor and use self-care."

def chat_reply(text: str) -> str:
    s = (text or "").lower()
    if "fever" in s:
        return "For fever, stay hydrated and consider paracetamol (500 mg). Seek care if high/lasting fever."
    if "headache" in s:
        return "For headache, rest and try ibuprofen (200–400 mg) with food unless contraindicated."
    if "diarrhea" in s:
        return "Use oral rehydration salts (ORS). Seek care if blood in stool or signs of dehydration."
    if "chest" in s and "pain" in s:
        return "Chest pain can be serious — seek emergency care immediately."
    return "Tell me your main symptoms, when they started, and anything that makes them better or worse."
