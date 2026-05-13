# apps/users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # POST /login/ → повертає access + refresh токени
    TokenRefreshView,     # POST /token/refresh/ → оновлює access токен
)
from apps.users.api import views

app_name = 'users'

urlpatterns = [
    # -------------------------------------------------------
    # Авторизація (JWT)
    # -------------------------------------------------------
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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