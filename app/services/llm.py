import os
from openai import OpenAI

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY"))

    def generate(self, prompt: str) -> str:
        if not self.client.api_key:
            return "LLM API key not configured."
        return f"Mock LLM response for: {prompt}"
