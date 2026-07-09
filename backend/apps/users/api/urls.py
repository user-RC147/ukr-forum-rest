# apps/users/urls.py
from django.urls import path
from apps.users.api.jwt.jwt_views import (
    CustomTokenObtainPairView,
    CookieTokenRefreshView,
)
from apps.users.api import views
from apps.users.api.views import views as file_views

app_name = 'users'

urlpatterns = [
    # -------------------------------------------------------
    # Авторизація (JWT)
    # -------------------------------------------------------
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('csrf/', file_views.get_csrf_token, name='get-csrf-token'),
    # -------------------------------------------------------
    # Акаунт
    # -------------------------------------------------------
    path('register/', views.RegisterView.as_view(), name='register'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete'),

    # -------------------------------------------------------
    # Профіль
    # -------------------------------------------------------
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # -------------------------------------------------------
    # Паролі
    # -------------------------------------------------------
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # apps/users/urls.py — додати в urlpatterns
    path('location/', views.LocationUpdateView.as_view(), name='location'),


]