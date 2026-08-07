import os
from pathlib import Path


def self_protection_check() -> dict:
    root = Path(__file__).resolve().parents[1]
    sensitive_files = [
        root / '.env',
        root / '.env.local',
        root / 'secrets.json',
    ]
    issues = []
    protected = []

    for path in sensitive_files:
        if path.exists():
            issues.append(f'{path.name} exists and should be protected')
        else:
            protected.append(path.name)

    return {
        'status': 'ok' if not issues else 'needs_attention',
        'runtime_guard': 'enabled',
        'protected_paths': protected,
        'issues': issues,
        'recommendations': [
            'Store secrets in a vault or environment manager.',
            'Restrict file permissions on sensitive files.',
            'Enable request rate limiting and auth on the API.',
        ],
    }
