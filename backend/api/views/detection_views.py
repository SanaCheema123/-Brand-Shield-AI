from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import DetectionInputSerializer, DetectionResultSerializer
from api.models.detection import DetectionResult
from api.models.report import Report
from ml.detectors.ensemble_detector import EnsembleDetector
from api.utils.response_utils import success_response, error_response

class DetectionView(APIView):
    """
    POST /api/detect/
    Accepts text, URL, or image input and runs multi-model brand impersonation detection.
    """
    def post(self, request):
        serializer = DetectionInputSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            detector = EnsembleDetector()
            result = detector.detect(
                input_type=data["input_type"],
                input_content=data["input_content"],
                target_brand=data.get("target_brand", ""),
            )

            # Save to DB
            detection = DetectionResult.objects.create(
                input_type=data["input_type"],
                input_content=data["input_content"],
                target_brand=data.get("target_brand", ""),
                gemini_score=result.get("gemini_score"),
                hf_score=result.get("hf_score"),
                ensemble_score=result.get("ensemble_score"),
                verdict=result["verdict"],
                confidence=result["confidence"],
                explanation=result.get("explanation", ""),
            )

            # Auto-generate report
            Report.objects.create(
                detection=detection,
                summary=result.get("explanation", ""),
                risk_level=result.get("risk_level", "low"),
                recommendation=result.get("recommendation", ""),
            )

            return success_response(
                DetectionResultSerializer(detection).data,
                status.HTTP_201_CREATED
            )

        except Exception as e:
            return error_response({"detail": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetectionDetailView(APIView):
    """GET /api/detect/<id>/"""
    def get(self, request, pk):
        try:
            detection = DetectionResult.objects.get(pk=pk)
            return success_response(DetectionResultSerializer(detection).data)
        except DetectionResult.DoesNotExist:
            return error_response({"detail": "Not found"}, status.HTTP_404_NOT_FOUND)
