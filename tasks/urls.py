"""
URL configuration for the tasks app.

Includes both API endpoints (for CRUD operations)
and a template-rendered view for displaying tasks in the UI.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TasksPageView

app_name = "tasks"

# Router for TaskViewSet API endpoints
router = DefaultRouter()
router.register(r"api", TaskViewSet, basename="task")

urlpatterns = [
    # API routes (e.g., /tasks/api/)
    path("", include(router.urls)),

    # Template-rendered page (e.g., /tasks/tasks/)
    path("tasks/", TasksPageView.as_view(), name="tasks_page"),
]
