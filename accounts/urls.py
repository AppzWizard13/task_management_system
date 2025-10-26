"""
URL configuration for the accounts app.

Includes frontend HTML pages and API endpoints for:
- User registration, login, logout
- Dashboard, profile, and change password
- JWT token refresh
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    DashboardView,
    DashboardAPIView,
    ProfilePageView,
    UserProfileAPIView,
    ChangePasswordPageView,
    ChangePasswordAPIView,
)

app_name = 'accounts'

urlpatterns = [
    # Frontend HTML pages
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('change-password/', ChangePasswordPageView.as_view(), name='change_password'),

    # API endpoints (JSON responses)
    path('api/dashboard/', DashboardAPIView.as_view(), name='api_dashboard'),
    path('api/profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/logout/', UserLogoutView.as_view(), name='api_logout'),

    # JWT token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
