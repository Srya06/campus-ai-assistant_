import os
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
from backend.app.core.config import settings
from backend.app.services.ai.base import BaseAIProvider

logger = logging.getLogger("gemini_provider")

class GeminiProvider(BaseAIProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (api_key or settings.GEMINI_API_KEY).strip()
        self.client: Optional[genai.Client] = None
        
        # If running unit tests or key is invalid/placeholder, treat as unavailable
        if os.getenv("TESTING") == "1" or not self.api_key or self.api_key.startswith("AIzaSyDNtNt") or "YOUR_GEMINI" in self.api_key:
            self.client = None
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Failed to create Google GenAI Client: {e}")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def generate_chat_response(
        self,
        prompt: str,
        system_instruction: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        if not self.is_available():
            return None

        try:
            contents = []
            if history:
                for msg in history[-6:]:
                    role = "user" if msg.get("role") == "user" else "model"
                    contents.append(types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=msg.get("content", ""))]
                    ))

            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            ))

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.6,
                max_output_tokens=1200
            )

            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=config
            )

            if response and response.text:
                return response.text
            return None
        except Exception as e:
            logger.warning(f"Gemini API call failed: {e}")
            return None

    def generate_document(
        self,
        doc_type: str,
        context: str,
        tone: str,
        length: str
    ) -> Optional[str]:
        if not self.is_available():
            return None

        prompt = f"""
TASK: Draft an academic {doc_type}
SITUATION/CONTEXT:
{context}

SPECIFICATIONS:
- Tone: {tone}
- Length: {length}
- Target: Academic faculty, Dean, HOD, or administration
- Formatting: Must include date, subject line, proper salutation, clear paragraph structure, and standard student sign-off with bracketed placeholders: [Your Name], [Roll Number], [Department].
- CRITICAL RULE: NEVER invent fake student names or registration numbers. Use editable bracketed placeholders.

Draft the document now:
"""
        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert university academic communications advisor.",
                    temperature=0.5,
                    max_output_tokens=1000
                )
            )
            if response and response.text:
                return response.text
            return None
        except Exception as e:
            logger.warning(f"Gemini document generation failed: {e}")
            return None
