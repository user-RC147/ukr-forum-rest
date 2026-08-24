from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from core.users.csrf_permission import CsrfPermission



class LogoutViewSet(ViewSet):

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            return [AllowAny(), CsrfPermission()]
        return [IsAuthenticated(), CsrfPermission()]
    
    @extend_schema()
    def create(self, request):
        refresh_token_str = request.COOKIES.get("refresh_token")

        if refresh_token_str:
            try:
                token = RefreshToken(refresh_token_str)
                token.blacklist()
            except TokenError:
                pass  # токен уже невалідний — це нормально, продовжуємо

        response = Response({"detail": "Ви вийшли з системи"}, status=status.HTTP_200_OK)

        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/api/auth/refresh/")

        return response