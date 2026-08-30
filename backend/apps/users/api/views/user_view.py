from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.users.dto.user_dto import CreateUserInDTO
from apps.users.dto._to_dto_user import _to_dto_user_in
from apps.users.services.user_service import UserService
from apps.users.api.serializers.user_serializer import (
    UserPublicOutSerializer,
    UserPrivatOutSerializer,
    UserShortOutSerializer,
)

from apps.users.api.serializers.register_serializer import (
    RegisterInSerializer,
    ProfileUpdateInSerializer,
)
from apps.users.services import UserService

from core.users.csrf_permission import CsrfPermission
from drf_spectacular.utils import extend_schema


class UserViewSet(ViewSet):

    def get_permissions(self):
        if self.action in ["create"]:  # "list", "retrieve",
            return [AllowAny(), CsrfPermission()]
        return [IsAuthenticated(), CsrfPermission()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = UserService()

    @action(detail=False, methods=["get"], url_path="profile")
    def profile(self, request):
        user = self._service.get_my_profile(request.user.id)
        serializer = UserPrivatOutSerializer(user)

        results = serializer.data

        return Response({"results": results}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="user_short")
    @extend_schema(request=UserShortOutSerializer(), responses=UserShortOutSerializer())
    def get_short_user(self, request):
        user = self._service.get_short_public_user(request.user.id)
        serializer = UserShortOutSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        all_user = self._service.get_many_public_user(ids=None)
        serializer = UserPublicOutSerializer(all_user, many=True)
        results = serializer.data
        return Response({"results": results}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = self._service.get_user_by_id(int(pk))
        serialazer = UserPublicOutSerializer(user)
        results = serialazer.data
        return Response({"results": results}, status=status.HTTP_200_OK)

    @extend_schema(request=RegisterInSerializer(), responses=RegisterInSerializer())
    def create(self, request):

        serializer = RegisterInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        _dto = CreateUserInDTO(
            username=data["username"],
            password=data["password"],
            display_name=data["display_name"],
            email=data["email"],
            referral_code=data.get("referral_code"),
            consent_given=data["consent_given"],
        )

        try:
            self._service.create(_dto)
        except ValueError:
            return Response(
                {"detail": "Помилка реєстрації"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Реєстрація успішна"},
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        request=ProfileUpdateInSerializer(), responses=RegisterInSerializer()
    )
    def update(self, request, pk=None):

        serialiser = ProfileUpdateInSerializer(data=request.data)
        serialiser.is_valid(raise_exception=True)

        dto = _to_dto_user_in(serialiser.validated_data)

        self._service.update_my_profile(dto, pk)

        return Response({"detail": "Профіль оновлено"}, status=status.HTTP_200_OK)

    # def partial_update(self, request, pk=None):
    #     pass

    def destroy(self, request, pk=None):
        user_id = getattr(request.user, "id", None)
        try:
            if int(pk) != user_id:
                return Response(
                    {"detail": "Ви не можете видаляти профіль"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except (ValueError, TypeError):
            return Response(
                {"detail": "Ви не доступу, якщо ви не залогінені!!"},
                status=status.HTTP_403_FORBIDDEN,
            )

        self._service.delete_user(user_id)

        return Response({"detail": "Профіль видалено"}, status=status.HTTP_200_OK)
