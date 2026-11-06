from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.api.serializers.password_reset_serializer import (
    PasswordResetConfirmInSerializer,
    PasswordResetRequestInSerializer,
)
from apps.users.services.password_reset_service import PasswordResetService
from core.users.csrf_permission import CsrfPermission


class PasswordResetViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny, CsrfPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = PasswordResetService()

    @extend_schema(
        request=PasswordResetRequestInSerializer(), responses=PasswordResetRequestInSerializer()
    )
    @action(detail=False, methods=["post"], url_path="request")
    def request_reset(self, request):
        serializer = PasswordResetRequestInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self._service.request_password_reset(serializer.validated_data["email"])

        return Response(
            {"detail": "Якщо email зареєстрований, лист надіслано"},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=PasswordResetConfirmInSerializer(), responses=PasswordResetConfirmInSerializer()
    )
    @action(detail=False, methods=["post"], url_path="confirm")
    def confirm_reset(self, request):
        serializer = PasswordResetConfirmInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self._service.confirm_password_reset(
                token=str(serializer.validated_data["token"]),
                new_password=serializer.validated_data["new_password"],
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Пароль успішно змінено"},
            status=status.HTTP_200_OK,
        )
