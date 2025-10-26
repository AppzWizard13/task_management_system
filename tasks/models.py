"""
Models for the tasks app.

Defines the Task model, which represents a user's individual task with optional attachments.
"""

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models


class Task(models.Model):
    """
    Represents a task created by a user.

    Each task contains a title, description, optional file attachment,
    and timestamps for creation and modification.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="User who created this task.",
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the task.",
    )
    description = models.TextField(
        help_text="Detailed description of the task.",
    )
    attachment = models.FileField(
        upload_to="task_attachments/%Y/%m/%d/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "txt",
                    "jpg",
                    "jpeg",
                    "png",
                    "zip",
                ]
            )
        ],
        help_text="Optional file attachment for the task.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the task was created.",
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the task was last modified.",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self):
        """Return a human-readable representation of the task."""
        return f"{self.title} - {self.user.username}"

    @property
    def attachment_filename(self):
        """Return the filename of the attachment without its full path."""
        if self.attachment:
            return self.attachment.name.split("/")[-1]
        return None
