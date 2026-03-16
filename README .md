# 🛡️ Brand Shield AI
### Multi-Model Brand Impersonation Detection System

> An AI-powered security platform that detects brand impersonation attempts in real-time using an ensemble of **Google Gemini 1.5 Flash** and **HuggingFace BART** models, served via a production-ready **Django REST API** with a **Streamlit** dashboard.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [API Reference](#-api-reference)
- [Detection Pipeline](#-detection-pipeline)
- [UI Screenshots](#-ui-screenshots)
- [Model Details](#-model-details)
- [Configuration](#-configuration)
- [Testing](#-testing)

---

## 🎯 Overview

**Brand Shield AI** is a production-grade cybersecurity tool designed to combat brand impersonation — one of the fastest-growing vectors in phishing and fraud attacks. It accepts three input types (text, URL, image description) and passes them through an ensemble of two AI models that independently score the content and combine their results for a final weighted verdict.

The system is fully modular: each AI model is an independent detector, the ensemble layer handles scoring and verdict logic, and the Django REST API exposes clean endpoints for any frontend or integration to consume.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Multi-Model Ensemble** | Gemini + HuggingFace vote independently; weighted average produces final score |
| **3 Input Modalities** | Accepts plain text/email, URLs, and image descriptions |
| **Real-Time Detection** | API responds in under 5 seconds for most inputs |
| **Explainability** | Red flags list + plain-English explanation returned with every verdict |
| **Risk Classification** | 4-tier risk levels: `low`, `medium`, `high`, `critical` |
| **Persistent Reports** | All detections stored in database; queryable via REST API |
| **Interactive Dashboard** | Streamlit UI with live charts, verdict badges, and score bars |
| **100% Free APIs** | Gemini Free Tier + HuggingFace Free Inference — no paid subscriptions required |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT FRONTEND                        │
│   Home Dashboard │ Threat Analysis │ Reports │ Security Insights │
└────────────────────────────┬────────────────────────────────────┘
                             │  HTTP REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO REST API                             │
│                                                                  │
│   POST /api/detect/    GET /api/reports/    GET /api/health/     │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                   ML PIPELINE                             │  │
│   │                                                          │  │
│   │  ┌─────────────────┐     ┌─────────────────────────┐    │  │
│   │  │ GeminiDetector  │     │  HuggingFaceDetector     │    │  │
│   │  │  (60% weight)   │     │     (40% weight)         │    │  │
│   │  └────────┬────────┘     └───────────┬─────────────┘    │  │
│   │           │                          │                   │  │
│   │           └──────────┬───────────────┘                   │  │
│   │                      ▼                                   │  │
│   │            ┌──────────────────┐                          │  │
│   │            │ EnsembleDetector │                          │  │
│   │            │  Weighted Score  │                          │  │
│   │            │  Verdict + Risk  │                          │  │
│   │            └──────────────────┘                          │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│                     SQLite / PostgreSQL                          │
└─────────────────────────────────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   Google Gemini 1.5 Flash         HuggingFace Inference API
   (aistudio.google.com)           (api-inference.huggingface.co)
```

---

## 🛠️ Tech Stack

### Backend
| Layer | Technology | Version |
|---|---|---|
| Web Framework | Django | 5.2 |
| REST API | Django REST Framework | 3.16 |
| CORS Handling | django-cors-headers | 4.9 |
| Database (Dev) | SQLite | Built-in |
| Database (Prod) | PostgreSQL | 15+ |
| Server | Gunicorn + WhiteNoise | — |

### AI / ML
| Component | Technology | Notes |
|---|---|---|
| Primary Model | Google Gemini 1.5 Flash | Free tier, reasoning-based |
| Secondary Model | HuggingFace BART-large-mnli | Free inference, zero-shot |
| Spam Detector | BERT SMS Spam Detection | Free inference |
| Explainability | LIME + SHAP | Local model explanations |

### Frontend
| Layer | Technology |
|---|---|
| UI Framework | Streamlit 1.35 |
| Charts | Plotly |
| Data Handling | Pandas |

---

## 📁 Project Structure

```
brand_impersonation_detection/
│
├── backend/                        # Django REST API
│   ├── core/
│   │   ├── settings.py             # All configuration (loads from .env)
│   │   ├── urls.py                 # Root URL routing
│   │   └── wsgi.py                 # WSGI entry point
│   │
│   ├── api/
│   │   ├── views/
│   │   │   ├── detection_views.py  # POST /api/detect/ — main detection endpoint
│   │   │   ├── report_views.py     # GET /api/reports/ — report listing
│   │   │   └── health_views.py     # GET /api/health/ — service health check
│   │   │
│   │   ├── models/
│   │   │   ├── detection.py        # DetectionResult DB model
│   │   │   ├── brand.py            # Brand registry model
│   │   │   └── report.py          # Report model (linked to detection)
│   │   │
│   │   ├── serializers/            # DRF serializers for input/output
│   │   └── utils/                  # Response helpers, validators
│   │
│   └── ml/
│       ├── detectors/
│       │   ├── gemini_detector.py  # Google Gemini integration
│       │   ├── hf_detector.py      # HuggingFace integration
│       │   └── ensemble_detector.py # Weighted ensemble logic
│       │
│       ├── preprocessing/          # Text, URL, image preprocessors
│       └── explainability/         # LIME and SHAP explainers
│
├── frontend/
│   └── app.py                      # Full Streamlit app (single file)
│
├── configs/
│   └── model_config.py             # Ensemble weights, risk thresholds
│
├── tests/
│   ├── unit/                       # Unit tests for detectors
│   └── integration/               # API endpoint tests
│
├── docs/                           # Additional documentation
├── scripts/                        # Setup and run shell scripts
├── .env.example                    # Environment variable template
├── docker-compose.yml              # Docker setup (optional)
└── Makefile                        # Shortcut commands
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python **3.11+**
- pip

### Step 1 — Clone / Extract the Project
```bash
cd "G:\Ahmad_projects\MARCH PROJECTS\brand_impersonation_detection"
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv --without-pip
venv\Scripts\python.exe -m ensurepip
```

### Step 3 — Activate Virtual Environment
```bash
# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### Step 4 — Install Dependencies
```bash
# Backend
.\venv\Scripts\pip3.exe install -r backend/requirements.txt

# Frontend
.\venv\Scripts\pip3.exe install -r frontend/requirements.txt
```

### Step 5 — Configure Environment Variables
```bash
copy .env.example .env
```

Open `.env` and fill in your API keys:

```env
GEMINI_API_KEY=your_gemini_key_here
HF_API_TOKEN=your_hf_token_here
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

> **Getting Free API Keys:**
> - **Gemini** → https://aistudio.google.com/app/apikey (sign in with Google, instant)
> - **HuggingFace** → https://huggingface.co/settings/tokens (free account required)

### Step 6 — Run Database Migrations
```bash
cd backend
..\venv\Scripts\python.exe manage.py makemigrations api
..\venv\Scripts\python.exe manage.py migrate
cd ..
```

---

## 🚀 Running the Application

Open **two separate terminals**.

**Terminal 1 — Backend API:**
```bash
cd backend
..\venv\Scripts\python.exe manage.py runserver
```
✅ API running at → `http://127.0.0.1:8000`

**Terminal 2 — Frontend UI:**
```bash
.\venv\Scripts\python.exe -m streamlit run frontend/app.py
```
✅ Dashboard running at → `http://localhost:8501`

---

## 📡 API Reference

### `POST /api/detect/`
Run brand impersonation detection on submitted content.

**Request Body:**
```json
{
  "input_type": "text",
  "input_content": "Dear customer, your PayPal account has been suspended. Click here to verify: http://paypa1.com",
  "target_brand": "PayPal"
}
```

| Field | Type | Required | Options |
|---|---|---|---|
| `input_type` | string | ✅ | `text`, `url`, `image` |
| `input_content` | string | ✅ | Max 5000 characters |
| `target_brand` | string | ❌ | Helps focus detection |

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "verdict": "impersonation",
    "confidence": 0.8340,
    "gemini_score": 0.92,
    "hf_score": 0.71,
    "ensemble_score": 0.8340,
    "risk_level": "high",
    "explanation": "URL uses typosquatting (paypa1 vs paypal). Urgent language pattern consistent with phishing.",
    "red_flags": ["Typosquatting domain", "Urgent account suspension claim", "Suspicious redirect link"],
    "recommendation": "Do NOT interact. This is likely a brand impersonation attack."
  }
}
```

---

### `GET /api/reports/`
Retrieve all past detection reports.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "detection_verdict": "impersonation",
      "detection_input_type": "text",
      "risk_level": "high",
      "summary": "...",
      "recommendation": "...",
      "created_at": "2026-03-11T22:30:00Z"
    }
  ]
}
```

---

### `GET /api/health/`
Service health check.

**Response:**
```json
{
  "status": "ok",
  "gemini_configured": true,
  "hf_configured": true,
  "version": "1.0.0"
}
```

---

## 🔬 Detection Pipeline

```
Input Received
     │
     ▼
┌────────────────────┐
│   Preprocessing    │  Clean text, normalize URL, extract metadata
└────────┬───────────┘
         │
    ┌────┴─────┐
    ▼          ▼
┌────────┐  ┌──────────────┐
│ Gemini │  │ HuggingFace  │   Run simultaneously
│  API   │  │ Inference    │
└───┬────┘  └──────┬───────┘
    │              │
    ▼              ▼
 Score: 0.92   Score: 0.71
    │              │
    └──────┬───────┘
           ▼
   Ensemble Weighting
   (0.92×0.6) + (0.71×0.4) = 0.836
           │
           ▼
   Verdict Mapping
   ≥0.70 → "impersonation"
   ≥0.40 → "suspicious"
   <0.40  → "safe"
           │
           ▼
   Save to Database + Return Response
```

### Ensemble Weights

| Model | Weight | Reason |
|---|---|---|
| Google Gemini 1.5 Flash | **60%** | Superior reasoning, context understanding |
| HuggingFace BART | **40%** | Fast, pattern-based classification |

### Verdict Thresholds

| Score Range | Verdict | Risk Level |
|---|---|---|
| `0.85 – 1.00` | Impersonation | 🔴 Critical |
| `0.70 – 0.84` | Impersonation | 🟠 High |
| `0.40 – 0.69` | Suspicious | 🟡 Medium |
| `0.00 – 0.39` | Safe | 🟢 Low |

---

## 🖥️ UI Screenshots

The Streamlit frontend has four pages:

| Page | Description |
|---|---|
| **Home Dashboard** | Project overview, feature cards, quick start guide |
| **Threat Analysis** | Submit text/URL/image for live detection |
| **Incident Reports** | Table of all past detections with verdict badges |
| **Security Insights** | Plotly pie chart and bar chart of detection statistics |

---

## 🤖 Model Details

### Google Gemini 1.5 Flash
- **Type:** Large Language Model (reasoning-based)
- **Task:** Structured JSON analysis of input for brand impersonation indicators
- **Prompt strategy:** Chain-of-thought with explicit JSON output schema
- **Cost:** Free tier via Google AI Studio

### HuggingFace BART-large-mnli
- **Type:** Zero-shot classification transformer
- **Task:** Classify input against labels: `brand impersonation`, `phishing attempt`, `legitimate content`
- **Cost:** Free via HuggingFace Inference API

---

## 🔧 Configuration

All model behavior is controlled via `configs/model_config.py`:

```python
ENSEMBLE_WEIGHTS = {
    "gemini": 0.6,
    "huggingface": 0.4,
}

VERDICT_THRESHOLDS = {
    "suspicious":     0.40,
    "impersonation":  0.70,
}

RISK_THRESHOLDS = {
    "medium":   0.40,
    "high":     0.70,
    "critical": 0.85,
}
```

To adjust model sensitivity, simply change these values without touching any other code.

---

## 🧪 Testing

```bash
# Run all tests
cd backend
..\venv\Scripts\python.exe manage.py test

# Test health endpoint manually
curl http://127.0.0.1:8000/api/health/

# Test detection endpoint manually
curl -X POST http://127.0.0.1:8000/api/detect/ \
  -H "Content-Type: application/json" \
  -d '{"input_type": "url", "input_content": "http://paypa1-secure.com", "target_brand": "PayPal"}'
```

---

## 👤 Author

**Ahmad** — AI/ML Engineer
- Project: Brand Shield AI
- Stack: Python · Django · Streamlit · Google Gemini · HuggingFace
- Date: March 2026

---

*Built for the MARCH PROJECTS series — production-ready AI security tooling.*
