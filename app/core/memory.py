import json
from datetime import datetime, timezone
from pathlib import Path


class Memory:
    def __init__(self, state_dir: str = "data"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.state_dir / "conversation_state.jsonl"

    def append_event(self, event: dict):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **event,
        }
        with self.file_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")

    def read(self) -> list[dict]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]
