# login_in_service.py
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.dto.login_in_dto import LoginOutDTO,_to_dto_login


class LoginInService:

    def login(self, username: str, password: str) -> LoginOutDTO:

        user = authenticate(username=username, password=password)

        if user is None:
            raise ValueError("Невірний логін або пароль")

        refresh = RefreshToken.for_user(user)

        dto = _to_dto_login(refresh)

        return dto

