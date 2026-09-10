from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from apps.users.api.serializers.email_confirm_serializer import ConfirmEmailInSerializer
from apps.users.services.email_confirm_service import EmailConfirmationTokenService

from rest_framework.permissions import IsAuthenticated, AllowAny
from core.users.csrf_permission import CsrfPermission
from drf_spectacular.utils import extend_schema


class ConfirmEmailView(ViewSet):

    def get_permissions(self):
        if self.action in ["create"]:  # "list", "retrieve",
            return [AllowAny(), CsrfPermission()]
        return [IsAuthenticated(), CsrfPermission()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = EmailConfirmationTokenService()

    # def list(self, request):
    #     pass

    @extend_schema(request=ConfirmEmailInSerializer())
    def create(self, request):
        serializer = ConfirmEmailInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        try:
            self._service.confirm_email(token)
        except ValueError:
            return Response(
                {"detail": "Токен недійсний або протермінований"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Email підтверджено"},
            status=status.HTTP_200_OK,
        )

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
