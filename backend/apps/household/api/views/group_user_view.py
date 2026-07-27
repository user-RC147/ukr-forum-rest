from email.headerregistry import Group
from tokenize import group
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.household.api.serializers import (
    GroupMemberOutSerializer,
    GroupOutSerializer,
    CreateGroupInSerializer,
)

from apps.household.dto.group_dto import CreateGroupInDTO, Group_Id_Name_InDTO
from apps.household.models.group import GroupMember
from apps.household.services.group_service import GroupService
from apps.household.dto import GroupOutDTO
from drf_spectacular.utils import extend_schema
from apps.household.api.serializers.group_serializer import Group_Id_InSerializer,CreateGroupInSerializer

from apps.shop import serializers


class GroupViewSet(viewsets.ViewSet):
    """
    Контролер для управління групами користувачів.
    Працює виключно через сервісний шар Чистої Архітектури.
    """

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = GroupService()

    # чи є користувач частиною групи
    # Викликаємо метод екземпляра сервісу, передаючи ID авторизованого юзера
    def auth_user_in_group(self, request): ...

    # def list(self, request): 
    #     grups = self._service.get_all_list()
    #     serializer = GroupOutSerializer(grups,many=True)
      
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
    def list(self,request):
        user_id = request.user.id
        serializer =Group_Id_InSerializer(data=request.query_params)

        serializer.is_valid(raise_exception=True)

        dto_group = Group_Id_Name_InDTO(
            id=serializer.validated_data.get('group_id'),
            name=serializer.validated_data.get('name')
        )

        group_members = self._service.get_all_group_member_by_user(dto_group,user_id=user_id)

        
        

        results = GroupOutSerializer(group_members,many=True).data

        # print('===/===/==/====/==/===/=====/=====/==/====================')
        # print('=================================================')
        # print("results")
        # print(results)
        # print('=================================================')

        return Response({'results':results},status=status.HTTP_200_OK)
  

    @extend_schema(request=CreateGroupInSerializer(), responses=GroupOutSerializer())
    def create(self, request):
        creator_id = request.user.id

        serializer = CreateGroupInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        dto = CreateGroupInDTO(
            name=data['name']
        )
        results = self._service.create_group(dto=dto,creator_id=creator_id)
         
        return Response({'results':results}, status=status.HTTP_201_CREATED)
     

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, group_id=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass