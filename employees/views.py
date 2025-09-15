# employees/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from django.db.models import Count, Avg

from .models import Department, Role, Employee, Attendance, Performance
from .serializers import (
    DepartmentSerializer, RoleSerializer, EmployeeListSerializer,
    EmployeeDetailSerializer, AttendanceSerializer, PerformanceSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "code"]
    filterset_fields = ["code"]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ["title", "level"]
    filterset_fields = ["is_management"]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department", "role", "manager").all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["department__code", "role__title", "status"]
    search_fields = ["first_name", "last_name", "email", "emp_id"]
    ordering_fields = ["hire_date", "salary", "first_name"]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return EmployeeListSerializer
        return EmployeeDetailSerializer

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def export_csv(self, request):
        qs = self.filter_queryset(self.get_queryset())
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="employees.csv"'
        writer = csv.writer(response)
        writer.writerow(["emp_id","first_name","last_name","email","department","role","manager","status","salary","hire_date"])
        for e in qs.iterator():
            writer.writerow([
                e.emp_id, e.first_name, e.last_name, e.email,
                e.department.name if e.department else "",
                e.role.title if e.role else "",
                e.manager.emp_id if e.manager else "",
                e.status, str(e.salary), str(e.hire_date)
            ])
        return response

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee").all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["employee__emp_id", "date", "status"]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("employee").all()
    serializer_class = PerformanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["employee__emp_id", "rating", "review_date"]
    search_fields = ["reviewer", "comments"]

# Analytics view
from rest_framework.views import APIView

class AnalyticsSummaryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        total_employees = Employee.objects.count()
        avg_salary = Employee.objects.aggregate(avg=Avg("salary"))["avg"] or 0

        by_dept_qs = Department.objects.annotate(count=Count("employees")).values("name", "count")
        by_dept = list(by_dept_qs)

        perf_qs = Performance.objects.values("rating").annotate(count=Count("id")).order_by("rating")
        perf_dist = {str(item["rating"]): item["count"] for item in perf_qs}

        data = {
            "total_employees": total_employees,
            "avg_salary": float(avg_salary),
            "employees_by_department": by_dept,
            "performance_distribution": perf_dist,
        }
        return Response(data)
