"""
Ensemble Detector: combines Gemini + HuggingFace predictions.
"""
from ml.detectors.gemini_detector import GeminiDetector
from ml.detectors.hf_detector import HuggingFaceDetector


RISK_THRESHOLDS = {"low": 0.3, "medium": 0.5, "high": 0.7, "critical": 0.85}
WEIGHTS = {"gemini": 0.6, "hf": 0.4}

RECOMMENDATIONS = {
    "safe": "No action needed. Input appears legitimate.",
    "suspicious": "Proceed with caution. Verify the source before interacting.",
    "impersonation": "Do NOT interact. This is likely a brand impersonation attack. Report to the affected brand.",
}


class EnsembleDetector:
    def __init__(self):
        self.gemini = GeminiDetector()
        self.hf = HuggingFaceDetector()

    def detect(self, input_type: str, input_content: str, target_brand: str = "") -> dict:
        gemini_result, hf_result = {}, {}

        if input_type == "text":
            gemini_result = self.gemini.detect_text(input_content, target_brand)
            hf_result = self.hf.detect_text_zero_shot(input_content, target_brand)

        elif input_type == "url":
            gemini_result = self.gemini.detect_url(input_content)
            hf_result = self.hf.detect_text_zero_shot(input_content)

        else:
            # Fallback: treat as text for image captions / metadata
            gemini_result = self.gemini.detect_text(input_content, target_brand)
            hf_result = self.hf.detect_text_zero_shot(input_content, target_brand)

        gemini_score = float(gemini_result.get("confidence", 0.0))
        hf_score = float(hf_result.get("confidence", 0.0))
        ensemble_score = (WEIGHTS["gemini"] * gemini_score) + (WEIGHTS["hf"] * hf_score)

        verdict = self._get_verdict(ensemble_score)
        risk_level = self._get_risk_level(ensemble_score)

        return {
            "gemini_score": gemini_score,
            "hf_score": hf_score,
            "ensemble_score": ensemble_score,
            "verdict": verdict,
            "confidence": round(ensemble_score, 4),
            "risk_level": risk_level,
            "explanation": gemini_result.get("explanation", ""),
            "red_flags": gemini_result.get("red_flags", []),
            "impersonated_brand": gemini_result.get("impersonated_brand"),
            "recommendation": RECOMMENDATIONS.get(verdict, ""),
        }

    def _get_verdict(self, score: float) -> str:
        if score >= 0.7:
            return "impersonation"
        elif score >= 0.4:
            return "suspicious"
        return "safe"

    def _get_risk_level(self, score: float) -> str:
        if score >= 0.85:
            return "critical"
        elif score >= 0.7:
            return "high"
        elif score >= 0.4:
            return "medium"
        return "low"
