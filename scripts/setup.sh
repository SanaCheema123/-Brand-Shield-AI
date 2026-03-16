#!/bin/bash
echo "=== Brand Impersonation Detection Setup ==="

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend deps
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# Install frontend deps
echo "Installing frontend dependencies..."
pip install -r frontend/requirements.txt

# Setup Django
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
cd ..

# Copy env
cp .env.example .env
echo ""
echo "✅ Setup complete!"
echo "📝 Add your API keys to .env:"
echo "   GEMINI_API_KEY=  → https://aistudio.google.com/app/apikey"
echo "   HF_API_TOKEN=    → https://huggingface.co/settings/tokens"
