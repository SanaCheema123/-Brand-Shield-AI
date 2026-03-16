from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class HealthCheckView(APIView):
    """GET /api/health/ - Check if service is running"""
    def get(self, request):
        return Response({
            "status": "ok",
            "gemini_configured": bool(settings.GEMINI_API_KEY),
            "hf_configured": bool(settings.HF_API_TOKEN),
            "version": "1.0.0",
        })
