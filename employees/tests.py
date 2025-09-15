# employees/tests.py
from django.test import TestCase
from employees.models import Department, Role, Employee

class EmployeeModelTests(TestCase):
    def test_create_employee(self):
        d = Department.objects.create(name="Test Dept", code="TST")
        r = Role.objects.create(title="Tester", level="Junior")
        emp = Employee.objects.create(
            emp_id="EMP999",
            first_name="Test",
            last_name="User",
            email="test.user@example.com",
            hire_date="2020-01-01",
            department=d,
            role=r,
            salary=50000
        )
        self.assertEqual(str(emp), "EMP999 - Test User")
