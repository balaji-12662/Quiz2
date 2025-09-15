# Employee Management & Analytics System

A Django REST Framework (DRF) based Employee Management System with analytics visualization using **Chart.js** on the frontend.

---

## 🚀 Features
- Manage **Departments, Roles, Employees, Attendance, Performance**
- REST API endpoints with **CRUD support**
- Analytics summary (`/api/analytics/summary/`) including:
  - Employees count by department
  - Performance distribution
  - Average salary
- CSV export for employees
- Interactive **charts** (bar + pie) using Chart.js on the frontend

---

## 🛠️ Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: SQLite (default, but can switch to PostgreSQL/MySQL)
- **Frontend**: HTML + Chart.js (basic analytics dashboard)
- **Tools**: Django Filters, Postman for API testing

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/employee-analytics.git
cd employee-analytics
2️⃣ Create Virtual Environment & Install Dependencies
bash
Copy code
python -m venv venv
venv\Scripts\activate      # on Windows

pip install -r requirements.txt
3️⃣ Apply Migrations
bash
Copy code
python manage.py migrate
4️⃣ Run Development Server
bash
Copy code
python manage.py runserver
Server will start at: http://127.0.0.1:8000/

📡 API Endpoints
Departments
GET /api/departments/ → List departments

POST /api/departments/ → Create department

json
Copy code
{ "name": "IT", "code": "IT01" }
Roles
GET /api/roles/

POST /api/roles/

json
Copy code
{ "title": "Developer", "level": "Junior", "is_management": false }
Employees
GET /api/employees/ → List employees

POST /api/employees/ → Create employee

json
Copy code
{
  "emp_id": "E100245",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "department": "IT",
  "role": "Developer",
  "salary": 60000,
  "hire_date": "2025-09-15"
}
✅ Note: Departments and Roles must exist before creating Employees.

📊 Analytics API
GET /api/analytics/summary/

Example response:

json
Copy code
{
  "total_employees": 12,
  "avg_salary": 58000.0,
  "employees_by_department": [
    {"name": "IT", "count": 5},
    {"name": "HR", "count": 3}
  ],
  "performance_distribution": {
    "1": 2,
    "2": 4,
    "3": 3,
    "4": 2,
    "5": 1
  }
}
📈 Analytics Dashboard (Frontend)
Visit:
👉 http://127.0.0.1:8000/

You’ll see:

Bar chart → Employees per department

Pie chart → Performance distribution

📂 Project Structure
bash
Copy code
employee_project/
│── employees/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│── templates/
│   ├── index.html   # Chart.js Dashboard
│── manage.py
│── requirements.txt
│── README.md
📬 Testing with Postman
Create Department

POST /api/departments/

json
Copy code
{ "name": "IT", "code": "IT01" }
Create Role

POST /api/roles/

json
Copy code
{ "title": "Developer", "level": "Junior", "is_management": false }
Create Employee

POST /api/employees/

json
Copy code
{
  "emp_id": "E100245",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "department": "IT",
  "role": "Developer",
  "salary": 60000,
  "hire_date": "2025-09-15"
}
Check Analytics

GET /api/analytics/summary/

📝 License
This project is open-source. You can use, modify, and distribute it freely.



---

Do you also want me to include a **step-by-step Postman test collection (export JSON file)** so you can import it dire
