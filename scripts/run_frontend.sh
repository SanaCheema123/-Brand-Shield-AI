#!/bin/bash
source venv/bin/activate
echo "Starting Streamlit frontend on http://localhost:8501 ..."
cd frontend && streamlit run app.py --server.port 8501
