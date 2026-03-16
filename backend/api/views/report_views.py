from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.report import Report
from api.serializers.report_serializers import ReportSerializer
from api.utils.response_utils import success_response, error_response

class ReportListView(APIView):
    """GET /api/reports/ - List all detection reports"""
    def get(self, request):
        reports = Report.objects.select_related("detection").all()
        serializer = ReportSerializer(reports, many=True)
        return success_response(serializer.data)

class ReportDetailView(APIView):
    """GET /api/reports/<id>/"""
    def get(self, request, pk):
        try:
            report = Report.objects.select_related("detection").get(pk=pk)
            return success_response(ReportSerializer(report).data)
        except Report.DoesNotExist:
            return error_response({"detail": "Not found"}, status.HTTP_404_NOT_FOUND)
