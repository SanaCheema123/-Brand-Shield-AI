from rest_framework import serializers
from api.models.detection import DetectionResult

class DetectionInputSerializer(serializers.Serializer):
    """Input payload for detection request."""
    input_type = serializers.ChoiceField(choices=["text", "url", "image"])
    input_content = serializers.CharField(max_length=5000)
    target_brand = serializers.CharField(max_length=255, required=False, default="")

class DetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = "__all__"
