# EYRIC RYTHOS AI — Project State Snapshot

Project: EYRIC RYTHOS AI
Repository: C:\Users\avina\OneDrive\Documents\GitHub\EYRIC-RYTHOS-AI
Saved on: 2026-07-12

## Current status
- Local FastAPI app is running and reachable at http://127.0.0.1:8000
- Public temporary URL available: https://afraid-parrots-burn.loca.lt
- Security hardening is active: API key auth and rate limiting are implemented
- Landing page and demo analyzer are available at /
- Regression tests are passing

## What has been completed
- Built a restart-safe FastAPI-based security AI prototype
- Added threat analysis, site assessment, workflow execution, self-protection, and public guard posture logic
- Added persistent JSONL memory/logging for restart-safe operation
- Added security layer with API key validation and rate limiting
- Added a public-facing landing page and demo UI
- Verified the app with unit tests

## Core files
- app/main.py
- app/core/agent.py
- app/core/memory.py
- app/core/security.py
- app/tools/website_protection.py
- app/tools/workflow_templates.py
- app/tools/self_protection.py
- app/tools/public_guard.py
- run.py
- service.py
- tests/test_agent.py
- tests/test_security_layers.py
- tests/test_workflows.py

## Resume commands
Run from PowerShell:

```powershell
cd C:\Users\avina\OneDrive\Documents\GitHub\EYRIC-RYTHOS-AI
$env:PYTHONPATH='.'
python run.py
```

Verify:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expose publicly for testing:

```powershell
npx -y localtunnel --port 8000
```

## Environment notes
- API key is read from the API_KEY environment variable if set.
- Rate limiting defaults are controlled by RATE_LIMIT and RATE_WINDOW.
- Example:

```powershell
$env:API_KEY='your-secret-key'
```

## Current public access
- Local: http://127.0.0.1:8000
- Public test URL: https://afraid-parrots-burn.loca.lt

## Next recommended work
- Add real authentication and admin controls
- Add GitHub/webhook integrations
- Add monitoring and alerting
- Add custom domain and permanent hosting

## Quick summary for future handoff
Use this project as the base for EYRIC RYTHOS AI. The current implementation is a public-ready security AI prototype with threat analysis, defensive posture checks, workflow automation, and a browser-accessible front end.
