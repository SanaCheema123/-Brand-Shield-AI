"""
HuggingFace Inference API Detector — FREE tier, available in Pakistan
Get your token at: https://huggingface.co/settings/tokens
"""
import requests
from django.conf import settings


HF_MODELS = {
    "zero_shot": "facebook/bart-large-mnli",           # Zero-shot classification
    "phishing": "ealvaradob/bert-finetuned-phishing",  # Phishing URL detection
    "spam": "mrm8488/bert-tiny-finetuned-sms-spam-detection",  # Spam text
}


class HuggingFaceDetector:
    def __init__(self):
        self.token = settings.HF_API_TOKEN
        self.base_url = settings.HF_INFERENCE_URL
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def _query(self, model_id: str, payload: dict) -> dict:
        url = f"{self.base_url}/{model_id}"
        response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    def detect_text_zero_shot(self, text: str, target_brand: str = "") -> dict:
        """Use zero-shot classification to detect impersonation."""
        labels = ["brand impersonation", "phishing attempt", "legitimate content"]
        if target_brand:
            labels.insert(0, f"{target_brand} impersonation")

        result = self._query(HF_MODELS["zero_shot"], {
            "inputs": text[:512],
            "parameters": {"candidate_labels": labels}
        })

        scores = dict(zip(result.get("labels", []), result.get("scores", [])))
        impersonation_score = max(
            scores.get("brand impersonation", 0),
            scores.get("phishing attempt", 0),
            scores.get(f"{target_brand} impersonation", 0) if target_brand else 0,
        )
        return {
            "is_impersonation": impersonation_score > 0.5,
            "confidence": impersonation_score,
            "scores": scores,
        }

    def detect_spam(self, text: str) -> dict:
        """Detect spam / phishing in text."""
        result = self._query(HF_MODELS["spam"], {"inputs": text[:512]})
        if isinstance(result, list) and result:
            labels = {item["label"]: item["score"] for item in result[0]}
            spam_score = labels.get("spam", labels.get("SPAM", 0))
            return {"is_spam": spam_score > 0.5, "confidence": spam_score}
        return {"is_spam": False, "confidence": 0.0}
