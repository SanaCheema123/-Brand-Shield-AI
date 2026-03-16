from django.urls import path
from api.views.detection_views import DetectionView, DetectionDetailView
from api.views.report_views import ReportListView, ReportDetailView
from api.views.health_views import HealthCheckView

urlpatterns = [
    path("detect/", DetectionView.as_view(), name="detect"),
    path("detect/<int:pk>/", DetectionDetailView.as_view(), name="detect-detail"),
    path("reports/", ReportListView.as_view(), name="reports"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="report-detail"),
    path("health/", HealthCheckView.as_view(), name="health"),
]
