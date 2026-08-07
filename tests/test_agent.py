import json
import tempfile
import unittest
from pathlib import Path

from app.core.agent import Agent


class AgentTests(unittest.TestCase):
    def test_detects_suspicious_activity_and_persists_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            agent = Agent(state_dir=tmpdir)
            result = agent.analyze_message("Suspicious brute force login attempt and phishing email detected")

            self.assertEqual(result["category"], "credential_attack")
            self.assertGreaterEqual(result["severity"], 3)
            self.assertIn("MFA", result["recommended_actions"][0])
            self.assertTrue(Path(tmpdir, "conversation_state.jsonl").exists())

            with open(Path(tmpdir, "conversation_state.jsonl"), "r", encoding="utf-8") as handle:
                lines = [json.loads(line) for line in handle if line.strip()]

            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0]["category"], "credential_attack")


if __name__ == "__main__":
    unittest.main()
