# Model configuration for ensemble detection

ENSEMBLE_WEIGHTS = {
    "gemini": 0.6,   # Gemini gets more weight (better at reasoning)
    "huggingface": 0.4,
}

VERDICT_THRESHOLDS = {
    "safe": 0.0,
    "suspicious": 0.40,
    "impersonation": 0.70,
}

RISK_THRESHOLDS = {
    "low": 0.0,
    "medium": 0.40,
    "high": 0.70,
    "critical": 0.85,
}

# HuggingFace model IDs (all free)
HF_MODELS = {
    "zero_shot_classifier": "facebook/bart-large-mnli",
    "phishing_detector": "ealvaradob/bert-finetuned-phishing",
    "spam_detector": "mrm8488/bert-tiny-finetuned-sms-spam-detection",
}

# Gemini settings
GEMINI_MAX_TOKENS = 1024
GEMINI_TEMPERATURE = 0.1   # Low temp for consistent analysis
