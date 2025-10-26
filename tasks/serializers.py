"""
Serializers for the tasks app.

Includes serializers for detailed and lightweight task representations.
"""

from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for full task details, used for create, retrieve, update, and delete operations.
    """

    user = serializers.StringRelatedField(read_only=True)
    attachment_filename = serializers.ReadOnlyField()
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "attachment",
            "attachment_filename",
            "attachment_url",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["id", "user", "created_at", "modified_at"]

    def get_attachment_url(self, obj):
        """Return the full absolute URL for the attached file, if available."""
        if obj.attachment:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.attachment.url) if request else obj.attachment.url
        return None

    def validate_title(self, value):
        """Ensure the task title is not empty or whitespace."""
        cleaned_value = value.strip()
        if not cleaned_value:
            raise serializers.ValidationError("Title cannot be empty.")
        return cleaned_value

    def validate_description(self, value):
        """Ensure the task description is not empty or whitespace."""
        cleaned_value = value.strip()
        if not cleaned_value:
            raise serializers.ValidationError("Description cannot be empty.")
        return cleaned_value


class TaskListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing tasks (optimized for list views).
    """

    user = serializers.StringRelatedField(read_only=True)
    attachment_filename = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "attachment",
            "attachment_filename",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["id", "user", "created_at", "modified_at"]

    def get_attachment_filename(self, obj):
        """Return only the filename of the attached file."""
        return obj.attachment_filename
