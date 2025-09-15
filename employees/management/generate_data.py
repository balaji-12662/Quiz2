# employees/management/commands/generate_data.py
import random
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import date, timedelta
from employees.models import Department, Role, Employee, Attendance, Performance
from django.db import transaction

fake = Faker()

class Command(BaseCommand):
    help = "Generate synthetic departments, roles, employees, attendance and performance data"

    def add_arguments(self, parser):
        parser.add_argument("--employees", type=int, default=5, help="Number of employees to create")

    def handle(self, *args, **options):
        n_employees = options["employees"]
        self.stdout.write("Generating data...")

        with transaction.atomic():
            # create departments
            depts = []
            for code, name in [("ENG","Engineering"), ("HR","Human Resources"), ("SLS","Sales")]:
                dept, _ = Department.objects.get_or_create(code=code, defaults={
                    "name": name,
                    "location": fake.city(),
                    "description": fake.sentence(),
                    "contact_email": fake.company_email(),
                    "phone": fake.phone_number(),
                })
                depts.append(dept)

            # create roles
            roles = []
            role_data = [
                ("Software Engineer", "Mid", False, 40000, 90000),
                ("HR Manager", "Senior", True, 50000, 120000),
                ("Sales Executive", "Junior", False, 30000, 70000),
            ]
            for title, level, is_mgmt, min_s, max_s in role_data:
                r, _ = Role.objects.get_or_create(title=title, level=level, defaults={
                    "is_management": is_mgmt,
                    "min_salary": min_s,
                    "max_salary": max_s,
                    "responsibilities": fake.text(max_nb_chars=200)
                })
                roles.append(r)

            # create employees
            employees = []
            for i in range(n_employees):
                first = fake.first_name()
                last = fake.last_name()
                emp_id = f"EMP{1000+i}"
                email = f"{first.lower()}.{last.lower()}{i}@example.com"
                dept = random.choice(depts)
                role = random.choice(roles)
                salary = random.randint(int(role.min_salary)+5000, max(int(role.max_salary)-5000, int(role.min_salary)+5000))
                hire_date = fake.date_between(start_date='-5y', end_date='today')
                emp, created = Employee.objects.get_or_create(emp_id=emp_id, defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "phone": fake.phone_number(),
                    "dob": fake.date_of_birth(minimum_age=22, maximum_age=60),
                    "hire_date": hire_date,
                    "department": dept,
                    "role": role,
                    "status": "active",
                    "salary": salary,
                    "address": fake.address(),
                    "notes": fake.sentence(),
                })
                employees.append(emp)

            # set random manager relationships
            for emp in employees:
                if random.random() < 0.3:
                    emp.manager = random.choice(employees)
                    emp.save()

            # attendance: last 30 days, for each employee add 10 random days
            for emp in employees:
                for _ in range(10):
                    d = date.today() - timedelta(days=random.randint(1,30))
                    try:
                        Attendance.objects.create(
                            employee=emp,
                            date=d,
                            check_in=fake.time_object(),
                            check_out=fake.time_object(),
                            work_hours=round(random.uniform(6,9),2),
                            status=random.choice(["present","remote","absent"]),
                            notes=fake.sentence()
                        )
                    except Exception:
                        # skip duplicates
                        pass

            # performance records
            for emp in employees:
                for months_ago in [3, 12]:
                    review_date = date.today() - timedelta(days=30*months_ago)
                    Performance.objects.create(
                        employee=emp,
                        review_date=review_date,
                        reviewer=fake.name(),
                        rating=random.randint(1,5),
                        goals_set=fake.paragraph(nb_sentences=2),
                        goals_met=random.choice([True, False]),
                        score=round(random.uniform(50,100),2),
                        comments=fake.sentence()
                    )

        self.stdout.write(self.style.SUCCESS("Data generation complete."))
