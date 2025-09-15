# employees/urls.py
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, RoleViewSet, EmployeeViewSet,
    AttendanceViewSet, PerformanceViewSet, AnalyticsSummaryAPIView
)
from django.urls import path, include

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"roles", RoleViewSet)
router.register(r"employees", EmployeeViewSet, basename="employees")
router.register(r"attendance", AttendanceViewSet)
router.register(r"performance", PerformanceViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/analytics/summary/", AnalyticsSummaryAPIView.as_view(), name="analytics-summary"),
]
