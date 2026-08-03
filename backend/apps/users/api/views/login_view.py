# login_view.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.conf import settings

from drf_spectacular.utils import extend_schema

from apps.users.api.serialazers.login_in_serializer import LoginInSerializer
from apps.users.services.login_in_service import LoginInService


class LoginViewSet(ViewSet):
    
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = LoginInService()

    @extend_schema(request=LoginInSerializer, responses=LoginInSerializer)
    def create(self, request):        

        serializer = LoginInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Виклик Service — уся бізнес-логіка (перевірка пароля, видача токенів)
        try:
            dto = self._service.login(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
        except ValueError:
            return Response(
                {"detail": "Невірний логін або пароль"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3. Формування HTTP-відповіді + встановлення cookies
        response = Response({"detail": "Успішний вхід"}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=dto.access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=60 * 15,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=dto.refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=60 * 60 * 24 * 14,
            path="/api/auth/refresh/",
        )

        return response
