"""
User authentication, profile management, and dashboard views.

Includes:
- Frontend HTML views (TemplateView)
- API endpoints (APIView, generics)
- JWT authentication, login/logout, and profile update operations.
"""

from datetime import timedelta

from django.contrib.auth import login, logout
from django.db.models import Count
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import (
    ChangePasswordSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)


class DashboardView(TemplateView):
    """
    Dashboard HTML page.

    Renders template; JavaScript handles data fetching.
    """
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """Return context data for the dashboard page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Dashboard'
        return context


class ProfilePageView(TemplateView):
    """
    Profile HTML page.

    Authenticated users only. JavaScript handles data fetching.
    """
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        """Return context data for the profile page."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Profile'
        return context


class ChangePasswordPageView(TemplateView):
    """
    Change password HTML page.

    Authenticated users only.
    """
    template_name = 'accounts/change_password.html'

    def get_context_data(self, **kwargs):
        """Return context data for change password page."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['page_title'] = 'Change Password'
        return context


class DashboardAPIView(APIView):
    """
    API endpoint for dashboard statistics.

    GET /accounts/api/dashboard/
    Requires JWT authentication.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch dashboard statistics for the authenticated user."""
        user = request.user

        from tasks.models import Task  # Avoid circular import

        total_users = CustomUser.objects.filter(is_active=True).count()
        total_tasks = Task.objects.count()
        user_tasks = Task.objects.filter(user=user)
        user_task_count = user_tasks.count()

        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_tasks_count = user_tasks.filter(created_at__gte=seven_days_ago).count()

        top_assignees = (
            CustomUser.objects.annotate(task_count=Count('tasks'))
            .filter(task_count__gt=0)
            .order_by('-task_count')[:5]
        )

        latest_tasks = user_tasks.order_by('-created_at')[:5]

        return Response({
            'user': UserProfileSerializer(user).data,
            'stats': {
                'total_users': total_users,
                'total_tasks': total_tasks,
                'user_task_count': user_task_count,
                'recent_tasks_count': recent_tasks_count,
            },
            'top_assignees': [
                {
                    'id': assignee.id,
                    'username': assignee.username,
                    'email': assignee.email,
                    'task_count': assignee.task_count,
                }
                for assignee in top_assignees
            ],
            'latest_tasks': [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description[:100],
                    'created_at': task.created_at,
                }
                for task in latest_tasks
            ],
        }, status=status.HTTP_200_OK)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.

    GET: Render registration page.
    POST: Create new user and return JWT tokens.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        """Render the registration HTML page."""
        return render(
            request,
            self.template_name,
            {'page_title': 'User Registration'}
        )

    def create(self, request, *args, **kwargs):
        """Create a new user and generate JWT tokens."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'User registered successfully',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    User login endpoint.

    GET: Render login page.
    POST: Authenticate user, return JWT tokens, and create Django session.
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    template_name = 'accounts/jwt_login.html'

    def get(self, request, *args, **kwargs):
        """Render the login page."""
        return render(
            request,
            self.template_name,
            {'page_title': 'Task Management System Login'}
        )

    def post(self, request, *args, **kwargs):
        """Authenticate user and return JWT tokens."""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        login(request, user)

        return Response({
            'user': UserProfileSerializer(user).data,
            'message': 'Login successful',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    User logout endpoint.

    POST: Blacklist refresh token and clear Django session.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Logout user, clear session, and blacklist JWT refresh token."""
        refresh_token = request.data.get('refresh')
        logout(request)

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Token invalid or expired

        return Response(
            {'message': 'Logout successful'},
            status=status.HTTP_200_OK
        )


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the user profile.

    GET: Retrieve current user's profile.
    PUT/PATCH: Update profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return the currently authenticated user."""
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        """Retrieve user profile."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'user': serializer.data,
            'message': 'Profile retrieved successfully'
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Update user profile (partial or full)."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'user': serializer.data,
            'message': 'Profile updated successfully'
        }, status=status.HTTP_200_OK)


class ChangePasswordAPIView(APIView):
    """
    API endpoint to change password for authenticated users.

    POST: Change password.
    Required fields: old_password, new_password, confirm_password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Validate and update the user's password."""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not all([old_password, new_password, confirm_password]):
            return Response({'error': 'All fields are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'New passwords do not match'},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(new_password) < 8:
            return Response({'error': 'Password must be at least 8 characters long'},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if not user.check_password(old_password):
            return Response({'error': 'Current password is incorrect'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password changed successfully'},
                        status=status.HTTP_200_OK)
