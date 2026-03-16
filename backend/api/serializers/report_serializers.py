from rest_framework import serializers
from api.models.report import Report

class ReportSerializer(serializers.ModelSerializer):
    detection_verdict = serializers.CharField(source="detection.verdict", read_only=True)
    detection_input_type = serializers.CharField(source="detection.input_type", read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
