Based on your project structure, here's the updated **README.md** file:

```markdown
# Django Task Management System

A full-stack Django-based task management system with JWT authentication, Docker containerization, PostgreSQL database, and automated superuser creation.

## Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **User Management** - Registration, login, profile management
- ✅ **Task CRUD** - Create, read, update, delete tasks with file attachments
- 🔒 **Role-Based Access** - Admin dashboard and user-specific task views
- 🐳 **Docker Support** - Fully containerized with Docker Compose
- 🗄️ **PostgreSQL Database** - Production-ready database setup
- 👑 **Auto Superuser** - Automatically creates admin account on first run

## Requirements

- Docker 20.10+
- Docker Compose 2.0+

## Quick Start Guide

### 1. Clone the Repository

```
git clone https://github.com/AppzWizard13/task_management_system
cd GL-INFOTECH-TASK
```

### 2. Create Environment File

Copy the `.env.example` file to create your `.env` file:

```
cp .env.example .env
```

### 3. Build and Run the Project

```
docker compose up -d --build
```

**Note:** The application will automatically create a superuser account on the first container startup.

### 4. Access the Application

- **Application URL:** http://localhost:8000
- **Admin Dashboard:** http://localhost:8000/accounts/dashboard/

### 5. Default Admin Credentials

The system automatically creates a superuser with the following credentials:

- **Username:** `admin`
- **Password:** `admin`
- **Email:** `admin@admin.com`

⚠️ **Important:** Change the default admin password after first login by navigating to **Change Password** in the user menu.

## Project Structure

```
GL-INFOTECH-TASK/
├── accounts/              # User authentication & profile management
│   ├── migrations/        # Database migrations
│   ├── templates/         # Account-related HTML templates
│   ├── models.py          # User profile model
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # Authentication views & APIs
│   └── urls.py            # Account URL routing
│
├── tasks/                 # Task CRUD operations
│   ├── migrations/        # Database migrations
│   ├── templates/         # Task-related HTML templates
│   ├── models.py          # Task model
│   ├── serializers.py     # Task serializers
│   ├── views.py           # Task views & APIs
│   └── urls.py            # Task URL routing
│
├── task_management_system/  # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
│
├── templates/             # Global HTML templates
│   └── base.html          # Base template with navbar/sidebar
│
├── static/                # Static files (CSS, JS, images)
│   └── assets/            # Bootstrap theme assets
│
├── media/                 # User-uploaded files (task attachments)
│
├── staticfiles/           # Collected static files for production
│
├── .env.example           # Environment variables template
├── docker-compose.yml     # Docker orchestration
├── Dockerfile             # Docker image configuration
├── docker-entrypoint.sh   # Container startup script
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## API Endpoints

### Authentication
- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login (returns JWT tokens)
- `POST /accounts/api/logout/` - User logout
- `POST /accounts/token/refresh/` - Refresh JWT token

### Profile Management
- `GET /accounts/api/profile/` - Get user profile
- `PATCH /accounts/api/profile/` - Update user profile
- `POST /accounts/api/change-password/` - Change password

### Dashboard
- `GET /accounts/dashboard/` - Admin dashboard (HTML)
- `GET /accounts/api/dashboard/` - Dashboard data (JSON)

### Tasks
- `GET /tasks/tasks/` - Task list page (HTML)
- `GET /tasks/api/` - List all tasks (user-specific, JSON)
- `POST /tasks/api/` - Create new task
- `GET /tasks/api/{id}/` - Get task details
- `PATCH /tasks/api/{id}/` - Update task
- `DELETE /tasks/api/{id}/` - Delete task

## Environment Variables

Key environment variables in `.env`:

```
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=task_management_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Superuser Credentials (auto-created on first run)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin
DJANGO_SUPERUSER_EMAIL=admin@admin.com
```

## Development Commands

### Run Migrations

```
docker compose exec web python manage.py migrate
```

### Create Additional Superuser

```
docker compose exec web python manage.py createsuperuser
```

### Collect Static Files

```
docker compose exec web python manage.py collectstatic --noinput
```

### View Logs

```
docker compose logs -f web
```

### Access Django Shell

```
docker compose exec web python manage.py shell
```

### Stop the Application

```
docker compose down
```

### Stop and Remove Volumes

```
docker compose down -v
```

## Technologies Used

- **Backend:** Django 4.x, Django REST Framework
- **Database:** PostgreSQL 15
- **Authentication:** JWT (Simple JWT)
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Containerization:** Docker, Docker Compose
- **Static Files:** WhiteNoise (for serving static files)

## Application Features

### For Regular Users
- ✅ User registration and login
- ✅ Profile management (full name, DOB, gender, mobile, address)
- ✅ Password change functionality
- ✅ Create, view, edit, and delete tasks
- ✅ Upload file attachments to tasks
- ✅ View only their own tasks

### For Admin Users
- ✅ All regular user features
- ✅ Access to admin dashboard
- ✅ View system statistics
- ✅ Manage all users (via Django admin)

## Security Notes

1. ✅ Change default admin password immediately after first login
2. ✅ Use strong `SECRET_KEY` in production
3. ✅ Set `DEBUG=False` in production
4. ✅ Configure proper `ALLOWED_HOSTS` in production
5. ✅ Use environment-specific database credentials
6. ✅ Enable HTTPS in production
7. ✅ Set proper CORS headers for production


This updated README reflects your actual project structure from the image, including:
- ✅ Correct folder names (`GL-INFOTECH-TASK`)
- ✅ Accurate project structure with `accounts/`, `tasks/`, `task_management_system/`
- ✅ Mentions of `docker-entrypoint.sh` and other visible files
- ✅ Static files and media directory structure
- ✅ Complete feature breakdown for users and admins

