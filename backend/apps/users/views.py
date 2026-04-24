# from django.shortcuts import render


# # Наприклад, у backend/apps/users/views.py
# import logging

# # logger отримає налаштування з секції 'apps'
# logger = logging.getLogger('apps.' + __name__) 
# # Або просто:
# # logger = logging.getLogger('apps')

# logger.debug("Це тільки для розробки")
# logger.info("Користувач увійшов в систему")
# logger.error("Щось пішло не так", exc_info=True)

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.models import CustomUser
from apps.users.serializers import UserRegisterSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    # CreateAPIView — вбудований клас DRF для створення об'єктів (POST)
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    # AllowAny — реєстрація доступна всім, без авторизації
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    # RetrieveUpdateAPIView — для читання (GET) і оновлення (PUT/PATCH) профілю
    serializer_class = UserProfileSerializer
    # IsAuthenticated — тільки авторизований користувач бачить свій профіль
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Повертаємо профіль поточного користувача
        # request.user — це автоматично підставляє JWT токен
        return self.request.user