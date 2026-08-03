from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.users.services.user_service import UserService
from apps.users.api.serialazers.user_serializer import (
    UserShortOutSerializer,
    UserPublicOutSerializer,
    UserPrivatOutSerializer,
)

from apps.users.services import UserService


class UserViewSet(ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = UserService()


    @action(detail=False,methods=["get"],url_path="profile")
    def profile(self,request):
        user = self._service.get_my_profile(request.user.id)
        serializer = UserPrivatOutSerializer(user)

        results = serializer.data

        return Response({'results':results},status=status.HTTP_200_OK)


    def list(self, request):

        all_user = self._service.get_all_user()

        serializer = UserShortOutSerializer(all_user, many=True)

        results = serializer.data

        return Response({"results": results}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        user_id = int(request.user.id)

        pk = int(pk)
        user = self._service.get_user_by_id(pk)

        serialazer = UserPublicOutSerializer(user)

        results = serialazer.data

        return Response({"results": results}, status=status.HTTP_200_OK)

    # def create(self, request):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
