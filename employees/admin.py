# employees/admin.py
from django.contrib import admin
from .models import Department, Role, Employee, Attendance, Performance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name","code","location")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("title","level","is_management")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_id","first_name","last_name","email","department","role","status","salary")
    search_fields = ("emp_id","first_name","last_name","email")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("employee","date","status","work_hours")

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("employee","review_date","rating","score")
