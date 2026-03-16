# Setup Guide

## Prerequisites
- Python 3.10+
- pip

## 1. Get Free API Keys

### Google Gemini (Free)
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key → paste in `.env` as `GEMINI_API_KEY`

### HuggingFace (Free)
1. Register at https://huggingface.co/join
2. Go to https://huggingface.co/settings/tokens
3. Create a new token (Read access is enough)
4. Copy → paste in `.env` as `HF_API_TOKEN`

## 2. Install & Run
```bash
bash scripts/setup.sh   # installs everything
bash scripts/run_backend.sh    # Terminal 1
bash scripts/run_frontend.sh   # Terminal 2
```

## 3. Open in Browser
- Backend API: http://localhost:8000/api/health/
- Frontend UI: http://localhost:8501
