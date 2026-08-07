from urllib.parse import urlparse


def assess_website(url: str) -> dict:
    parsed = urlparse(url or "")
    host = parsed.netloc or parsed.path or "unknown"
    controls = [
        "Enforce HTTPS and HSTS for the site.",
        "Enable a WAF and rate limiting to reduce abuse.",
        "Monitor access logs for suspicious behavior.",
    ]
    if parsed.scheme != "https":
        controls.insert(0, "Redirect the site to HTTPS immediately.")

    return {
        "url": url,
        "host": host,
        "status": "review_required",
        "recommended_controls": controls,
    }
