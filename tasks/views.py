"""
Views for task management operations.

Includes:
- `TaskViewSet`: Provides CRUD API endpoints for tasks.
- `TasksPageView`: Renders the tasks list page for authenticated users.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskListSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for user tasks.

    Endpoints:
        - GET /tasks/ — List user's tasks
        - POST /tasks/ — Create new task
        - GET /tasks/{id}/ — Retrieve specific task
        - PUT/PATCH /tasks/{id}/ — Update task details
        - DELETE /tasks/{id}/ — Delete a task
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    filterset_fields = ["created_at"]
    ordering_fields = ["created_at", "modified_at", "title"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return tasks belonging to the authenticated user."""
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """Use a lighter serializer for list views."""
        return TaskListSerializer if self.action == "list" else TaskSerializer

    def perform_create(self, serializer):
        """Save the task with the current user."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Handle task creation and return a success message."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Task created successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """Handle task update with optional attachment removal."""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        if request.data.get("remove_attachment") == "true":
            if instance.attachment:
                instance.attachment.delete(save=False)
            instance.attachment = None
            instance.save()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": "Task updated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a task and return a confirmation message."""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_200_OK,
        )

    def list(self, request, *args, **kwargs):
        """List tasks with pagination and search/filter support."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "count": queryset.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class TasksPageView(LoginRequiredMixin, TemplateView):
    """
    Render the task list page for the logged-in user.

    Admin users see all tasks.
    Regular users see only their own tasks.
    """

    template_name = "tasks/tasks.html"

    def get_context_data(self, **kwargs):
        """Build context data for the tasks page."""
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_staff or user.is_superuser:
            tasks = Task.objects.all().order_by("-created_at")
        else:
            tasks = Task.objects.filter(user=user).order_by("-created_at")

        context["user"] = user
        context["tasks"] = tasks
        return context
