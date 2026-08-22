from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.conf import settings

from apps.users.services.refresh_service import RefreshService
from core.users.csrf_permission import CsrfPermission


class RefreshViewSet(ViewSet):

    permission_classes = [AllowAny, CsrfPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = RefreshService()

    def create(self, request):
        # 1. Дістати refresh_token із cookie (не з тіла запиту!)
        
        x_csrf_token = request.COOKIES.get('X-CSRFToken')
        #enforce_csrf(request)
        refresh_token_str = request.COOKIES.get("refresh_token")

        if refresh_token_str is None:
            return Response(
                {"detail": "Токен оновлення відсутній"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 2. Викликати Service, зловити помилку невалідного токена
        try:
            dto = self._service.refresh(refresh_token_str)
        except ValueError:
            return Response(
                {"detail": "Токен оновлення недійсний або протух"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3. Сформувати відповідь + перезаписати обидва cookie новими токенами
        response = Response({"detail": "Токен оновлено"}, status=status.HTTP_200_OK)


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
