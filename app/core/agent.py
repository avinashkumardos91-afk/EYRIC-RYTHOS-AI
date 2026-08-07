import os
from dotenv import load_dotenv
from app.core.memory import Memory
from app.tools.public_guard import public_ready_plan
from app.tools.self_protection import self_protection_check
from app.tools.website_protection import assess_website
from app.tools.workflow_templates import workflow_templates

load_dotenv()


class Agent:
    def __init__(self, state_dir: str | None = None):
        self.provider = os.getenv("MODEL_PROVIDER", "local-rule-based")
        self.memory = Memory(state_dir=state_dir or os.getenv("STATE_DIR", "data"))

    def analyze_message(self, message: str) -> dict:
        normalized = (message or "").strip().lower()
        if not normalized:
            return {
                "category": "general",
                "severity": 1,
                "summary": "No threat signal detected.",
                "recommended_actions": ["Continue monitoring the environment."],
            }

        if any(keyword in normalized for keyword in ["brute force", "credential stuffing", "phishing", "login attempt"]):
            result = {
                "category": "credential_attack",
                "severity": 4,
                "summary": "Possible credential-based attack detected.",
                "recommended_actions": [
                    "Enable MFA and reset affected credentials.",
                    "Review sign-in logs and block suspicious IPs.",
                    "Alert the security team for investigation.",
                ],
            }
        elif any(keyword in normalized for keyword in ["ransomware", "malware", "trojan", "suspicious executable"]):
            result = {
                "category": "malware_or_ransomware",
                "severity": 5,
                "summary": "Potential malware or ransomware activity identified.",
                "recommended_actions": [
                    "Isolate the affected host immediately.",
                    "Scan endpoints and quarantine suspicious files.",
                    "Preserve logs for incident response.",
                ],
            }
        elif any(keyword in normalized for keyword in ["sql injection", "xss", "ddos", "web attack"]):
            result = {
                "category": "web_attack",
                "severity": 3,
                "summary": "Web application attack pattern detected.",
                "recommended_actions": [
                    "Apply rate limiting and WAF protections.",
                    "Review firewall and request logs.",
                    "Patch vulnerable endpoints if needed.",
                ],
            }
        else:
            result = {
                "category": "suspicious_activity",
                "severity": 2,
                "summary": "Unusual activity observed that should be reviewed.",
                "recommended_actions": [
                    "Continue monitoring and correlate with other indicators.",
                    "Review recent network and authentication events.",
                ],
            }

        self.memory.append_event(result)
        return result

    def run(self, message: str) -> str:
        if not message.strip():
            return "Please provide a message."
        analysis = self.analyze_message(message)
        return (
            f"[{self.provider}] {analysis['summary']}\n"
            f"Category: {analysis['category']}\n"
            f"Severity: {analysis['severity']}"
        )

    def assess_site(self, url: str) -> dict:
        result = assess_website(url)
        self.memory.append_event({"event_type": "site_assessment", **result})
        return result

    def execute_workflow(self, workflow_name: str, payload: dict | None = None) -> dict:
        workflow = workflow_templates.get(workflow_name)
        if not workflow:
            return {"workflow": workflow_name, "status": "unknown_workflow"}

        result = workflow(payload or {})
        self.memory.append_event({"event_type": "workflow", "workflow": workflow_name, **result})
        return result

    def self_protect(self) -> dict:
        result = self_protection_check()
        self.memory.append_event({"event_type": "self_protection", **result})
        return result

    def public_guard_status(self) -> dict:
        result = public_ready_plan()
        self.memory.append_event({"event_type": "public_guard", **result})
        return result


def build_agent() -> Agent:
    return Agent()
