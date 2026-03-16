#!/bin/bash
source venv/bin/activate
echo "Starting Django backend on http://localhost:8000 ..."
cd backend && python manage.py runserver 0.0.0.0:8000
