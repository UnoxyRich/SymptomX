
# SymptomX (minimal, with Chat)

- Dark-only UI
- Symptom checker (`POST /api/diagnose`)
- Chat via WebSocket (`/ws/chat`) with HTTP fallback (`POST /api/chat`)
- Amazon link appears on hover for each medication
- i18n: English (default) and Chinese (switcher top-right)
- No Docker; Windows PowerShell runner included: `setup_and_run.ps1`

## Run (Windows)
1. Right-click `setup_and_run.ps1` → Run with PowerShell (or in terminal: `.\setup_and_run.ps1`).
2. Open http://127.0.0.1:8000

Optional: create `gemini.json` at repo root to store an API key:
```json
{ "api_key": "YOUR_GEMINI_KEY" }
```
This repo **does not require** the key to run.
