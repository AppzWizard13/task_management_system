
---

````markdown
# Django Task Management System

A full-stack Django-based task management system with JWT authentication, PostgreSQL support for production, and automatic superuser creation.

---

## Features

- JWT Authentication – Secure token-based authentication
- User Management – Registration, login, profile management
- Task CRUD – Create, read, update, delete tasks with file attachments
- Role-Based Access – Admin dashboard and user-specific task views
- Auto Superuser – Automatically creates an admin account on first run
- Dual DB Setup – SQLite for local development, PostgreSQL for production

---

## Requirements

- Python 3.10+
- pip
- virtualenv (recommended)

---

## Quick Start Guide

### 1. Clone the Repository

```bash
git clone https://github.com/AppzWizard13/task_management_system
cd task_management_system
````

### 2. Create Virtual Environment and Activate It

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the `.env.example` file to create your `.env`:

```bash
cp .env.example .env
```

Update the `.env` file as needed:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1


# Production Database (PostgreSQL for Render)
# DATABASE_ENGINE=django.db.backends.postgresql
# DATABASE_NAME=task_management_db
# DATABASE_USER=postgres
# DATABASE_PASSWORD=your-password
# DATABASE_HOST=your-render-db-host
# DATABASE_PORT=5432

# Auto Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
```

---

## Local Development Setup

### Run Migrations

```bash
python manage.py migrate
```

### Create Default Admin (if not auto-created)

```bash
python manage.py create_admin
```

### Start Development Server

```bash
python manage.py runserver
```

Access the app at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Default Admin Credentials

| Field    | Value             |
| -------- | ----------------- |
| Username | `admin`           |
| Password | `admin`           |
| Email    | `admin@admin.com` |

---

## Deployment on Render

Render uses PostgreSQL automatically (configure via environment variables).

### Build Command

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py create_admin
```

### Start Command

```bash
gunicorn task_management_system.wsgi:application
```

---

## Technologies Used

* **Backend:** Django 4.x, Django REST Framework
* **Database:** SQLite (local), PostgreSQL (production)
* **Auth:** JWT (Simple JWT)
* **Frontend:** HTML, CSS, JavaScript, Bootstrap 5

---

## Application Features

### Regular Users

* User registration & login
* Profile management (full name, DOB, gender, mobile, address)
* Password change functionality
* Create, view, edit, delete personal tasks
* File uploads for tasks

### Admin Users

* All regular user features
* Access to admin dashboard
* Manage all users and tasks via Django Admin
* View system-wide statistics

---

## API Testing

A ready-to-use Postman collection is included in the project root:

```
Task Management System API.postman_collection.json
```

---

## Project Structure

```
task_management_system/
│
├── accounts/                     # User management and auth
├── core/                         # Core utilities, management commands
├── tasks/                        # Task CRUD APIs
├── templates/                    # HTML templates
├── static/                       # Static files
├── media/                        # Uploaded files
├── db.sqlite3                    # Local development database
├── manage.py
├── requirements.txt
├── README.md
└── Task Management System API.postman_collection.json
```

---

## Common Commands

| Action               | Command                                    |
| -------------------- | ------------------------------------------ |
| Run migrations       | `python manage.py migrate`                 |
| Create superuser     | `python manage.py createsuperuser`         |
| Collect static files | `python manage.py collectstatic --noinput` |
| Run server           | `python manage.py runserver`               |
| Run Django shell     | `python manage.py shell`                   |

---

## Notes

* SQLite is used for local development simplicity.
* PostgreSQL will be used automatically in the live Render deployment.
* The project auto-creates a default admin if one doesn’t exist.

---

```

---


