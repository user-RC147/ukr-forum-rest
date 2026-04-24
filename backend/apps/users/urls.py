from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,   # POST /login/ → повертає access + refresh токени
    TokenRefreshView,      # POST /token/refresh/ → оновлює access токен
)
from apps.users import views

# app_name — простір імен, щоб не плутати з іншими модулями
app_name = 'users'

urlpatterns = [
    # Реєстрація
    path('register/', views.RegisterView.as_view(), name='register'),

    # Логін — JWT повертає два токени: access (короткий) і refresh (довгий)
    path('login/', TokenObtainPairView.as_view(), name='login'),

    # Оновлення access токена через refresh токен
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профіль поточного користувача
    path('profile/', views.ProfileView.as_view(), name='profile'),
]