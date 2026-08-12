import os
import secrets
import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, limit: int = 60, window_seconds: int = 60):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def allow(self, key: str) -> bool:
        now = time.time()
        window = self.requests[key]
        window[:] = [ts for ts in window if now - ts < self.window_seconds]
        if len(window) >= self.limit:
            return False
        window.append(now)
        return True


def is_production() -> bool:
    return os.getenv('PRODUCTION', '').strip().lower() in {'1', 'true', 'yes', 'on'}


def check_api_key(
    provided_key: str | None,
    expected_key: str | None,
    production: bool | None = None,
) -> bool:
    if production is None:
        production = is_production()
    if not expected_key:
        # Open when unconfigured so local development stays frictionless, but fail
        # closed under PRODUCTION: a missing key must never silently mean "public".
        return not production
    if not provided_key:
        return False
    # Constant-time comparison: a plain == leaks how many leading characters
    # matched via response timing, letting an attacker recover the key byte by byte.
    return secrets.compare_digest(provided_key, expected_key)
