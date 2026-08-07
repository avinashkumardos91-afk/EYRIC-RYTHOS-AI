import os
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.core.agent import build_agent
from app.core.security import RateLimiter, check_api_key

app = FastAPI(title="EYRIC RYTHOS AI")

allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_agent()
rate_limiter = RateLimiter(limit=int(os.getenv('RATE_LIMIT', '60')), window_seconds=int(os.getenv('RATE_WINDOW', '60')))
API_KEY = os.getenv('API_KEY')


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>EYRIC RYTHOS AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; background: #07111f; color: #f5f7fb; }
            .hero { padding: 3rem 1.5rem; max-width: 1000px; margin: 0 auto; }
            .card { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 1.25rem; margin-top: 1rem; }
            code { background: #0f172a; padding: 0.2rem 0.4rem; border-radius: 6px; }
            button { background: #38bdf8; color: #07111f; border: none; padding: 0.7rem 1rem; border-radius: 8px; cursor: pointer; font-weight: bold; }
            textarea, input { width: 100%; padding: 0.7rem; border-radius: 8px; border: 1px solid #334155; margin-top: 0.5rem; }
        </style>
    </head>
    <body>
        <div class=\"hero\">
            <h1>EYRIC RYTHOS AI</h1>
            <p>A public-ready security AI prototype for threat analysis, website protection guidance, workflow automation, and self-defense posture checks.</p>
            <div class=\"card\">
                <h2>Live demo</h2>
                <p>Try a sample threat report below.</p>
                <textarea id=\"message\" rows=\"4\">Suspicious login spike from many IPs and a malware download attempt.</textarea>
                <button onclick=\"runDemo()\">Analyze</button>
                <pre id=\"result\" style=\"white-space: pre-wrap; margin-top: 1rem;\"></pre>
            </div>
            <div class=\"card\">
                <h2>Endpoints</h2>
                <ul>
                    <li><code>/health</code> — health check</li>
                    <li><code>/chat</code> — chat analysis</li>
                    <li><code>/analyze</code> — structured threat analysis</li>
                    <li><code>/assess-site</code> — website protection posture</li>
                    <li><code>/public-guard</code> — self-protection status</li>
                </ul>
            </div>
        </div>
        <script>
            async function runDemo() {
                const message = document.getElementById('message').value;
                const result = document.getElementById('result');
                result.textContent = 'Analyzing...';
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();
                    result.textContent = JSON.stringify(data, null, 2);
                } catch (err) {
                    result.textContent = 'Demo failed: ' + err.message;
                }
            }
        </script>
    </body>
    </html>
    """


@app.get("/health")
def health():
    return {"status": "ok", "project": "EYRIC RYTHOS AI"}


@app.get("/dashboard")
def dashboard(request: Request):
    return {
        "service": "EYRIC RYTHOS AI",
        "security_mode": "public_ready",
        "rate_limit": rate_limiter.limit,
        "auth_enabled": bool(API_KEY),
    }


def _require_access(x_api_key: str | None):
    if not check_api_key(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail='Invalid API key')


@app.post("/chat")
def chat(payload: ChatRequest, x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    if not rate_limiter.allow(payload.message or 'default'):
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    response = agent.run(payload.message)
    return {"reply": response}


@app.post("/analyze")
def analyze(payload: ChatRequest, x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    if not rate_limiter.allow(payload.message or 'default'):
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    return agent.analyze_message(payload.message)


@app.post("/assess-site")
def assess_site(payload: dict, x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    if not rate_limiter.allow(payload.get('url', 'default')):
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    return agent.assess_site(payload.get("url", ""))


@app.post("/workflow")
def run_workflow(payload: dict, x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    if not rate_limiter.allow(payload.get('workflow', 'default')):
        raise HTTPException(status_code=429, detail='Rate limit exceeded')
    return agent.execute_workflow(payload.get("workflow", ""), payload.get("payload", {}))


@app.post("/self-protect")
def self_protect(payload: dict, x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    return agent.self_protect()


@app.get("/public-guard")
def public_guard(x_api_key: str | None = Header(default=None, alias='X-API-Key')):
    _require_access(x_api_key)
    return agent.public_guard_status()
