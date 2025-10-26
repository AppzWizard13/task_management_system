"""
Django admin configuration for CustomUser model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for managing CustomUser instances.

    Extends the default UserAdmin to include profile fields,
    timestamps, and custom list display/search options.
    """
    list_display = [
        'username',
        'email',
        'full_name',
        'mobile_number',
        'is_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'gender',
        'created_at',
    ]
    search_fields = [
        'username',
        'email',
        'full_name',
        'mobile_number',
    ]
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        (
            'Profile Information',
            {'fields': ('full_name', 'date_of_birth', 'gender', 'mobile_number', 'address')},
        ),
        (
            'Timestamps',
            {'fields': ('created_at', 'updated_at')},
        ),
    )

    readonly_fields = ['created_at', 'updated_at']

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'Profile Information',
            {'fields': ('email', 'full_name', 'date_of_birth', 'gender', 'mobile_number', 'address')},
        ),
    )
