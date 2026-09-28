"""
Modular LLM Service for REALITYCHECK AI
Supports OpenAI, Gemini, or fallback rule-based analyzer.
"""

import json
import os
import re
from typing import Dict, Any, Optional, List
from config import get_llm_key, LLM_PROVIDER, LLM_MODEL

class LLMService:
    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None, model: Optional[str] = None):
        self.api_key = get_llm_key(api_key)
        self.provider = provider or LLM_PROVIDER
        self.model = model or LLM_MODEL

    def is_configured(self) -> bool:
        """Check if LLM key is configured."""
        key = self.api_key or get_llm_key()
        return bool(key and key.strip() and key != "your_llm_api_key_here")

    def generate_json(self, prompt: str, system_prompt: str = "You are a factual web investigation assistant.") -> Optional[Dict[str, Any]]:
        """
        Send prompt to LLM and expect structured JSON response.
        If key is missing or API fails, returns None to trigger heuristic fallback.
        """
        if not self.is_configured():
            return None

        try:
            # Try OpenAI / OpenAI-compatible API
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model if self.model else "gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt + " ALWAYS respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            # If JSON response format isn't supported or API call failed, try regex extract
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo" if "4" in self.model else self.model,
                    messages=[
                        {"role": "system", "content": system_prompt + " Respond ONLY in JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )
                raw_text = response.choices[0].message.content
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if match:
                    return json.loads(match.group(0))
            except Exception:
                pass
            return None
