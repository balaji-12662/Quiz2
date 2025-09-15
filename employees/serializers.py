# employees/serializers.py
from rest_framework import serializers
from .models import Department, Role, Employee, Attendance, Performance


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = "__all__"


class EmployeeListSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    role = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = [
            "id", "emp_id", "first_name", "last_name", "email",
            "department", "role", "manager", "status", "salary", "hire_date"
        ]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    manager = EmployeeListSerializer(read_only=True)
    attendances = AttendanceSerializer(many=True, read_only=True)
    performances = PerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"


# 🔹 New serializer for create/update (accepts IDs or names)
class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(
        slug_field="name", queryset=Department.objects.all()
    )
    role = serializers.SlugRelatedField(
        slug_field="title", queryset=Role.objects.all()
    )
    manager = serializers.SlugRelatedField(
        slug_field="emp_id", queryset=Employee.objects.all(),
        allow_null=True, required=False
    )

    class Meta:
        model = Employee
        fields = [
            "id", "emp_id", "first_name", "last_name", "email",
            "department", "role", "manager", "status", "salary", "hire_date"
        ]


