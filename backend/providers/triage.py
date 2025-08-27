
from __future__ import annotations

# Levels: 'emergency' | 'urgent' | 'routine'
def triage_message(level: str) -> str:
    lvl = (level or '').strip().lower()
    if lvl == "emergency":
        return "⚠️ This may require urgent care. Seek emergency services immediately."
    if lvl == "urgent":
        return "Please see a clinician soon (within 24–48 hours)."
    return "This seems non-urgent. Monitor and use self-care."
