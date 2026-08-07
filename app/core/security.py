import os
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


def check_api_key(provided_key: str | None, expected_key: str | None) -> bool:
    if not expected_key:
        return True
    if not provided_key:
        return False
    return provided_key == expected_key
