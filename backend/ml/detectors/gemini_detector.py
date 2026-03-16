from google import genai
from django.conf import settings
import json, re


class GeminiDetector:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL  # gemini-1.5-flash

    def detect_text(self, text: str, target_brand: str = "") -> dict:
        brand_hint = f" Focus on impersonation of '{target_brand}'." if target_brand else ""
        prompt = f"""You are a brand impersonation detection expert.
Analyze the following text and determine if it is impersonating a legitimate brand.{brand_hint}

TEXT:
{text}

Respond ONLY in this JSON format:
{{
  "is_impersonation": true/false,
  "confidence": 0.0-1.0,
  "impersonated_brand": "brand name or null",
  "red_flags": ["flag1", "flag2"],
  "explanation": "brief explanation"
}}"""
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return self._parse_response(response.text)

    def detect_url(self, url: str) -> dict:
        prompt = f"""Analyze this URL for brand impersonation / phishing:
URL: {url}

Respond ONLY in this JSON format:
{{
  "is_impersonation": true/false,
  "confidence": 0.0-1.0,
  "impersonated_brand": "brand name or null",
  "red_flags": ["flag1"],
  "explanation": "brief explanation"
}}"""
        response = self.client.models.generate_content(model=self.model, contents=prompt)
        return self._parse_response(response.text)

    def _parse_response(self, text: str) -> dict:
        try:
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        return {"is_impersonation": False, "confidence": 0.0,
                "impersonated_brand": None, "red_flags": [], "explanation": text}