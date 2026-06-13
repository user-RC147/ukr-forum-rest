import stat
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from rest_framework import status

from apps.household.apps import HouseholdConfig
from apps.household.api.serializers.asset_serializer import AssetSerializer
from apps.household.dto.asset_dto import CreateAssetDTO
from apps.household.services import AssetService


class AssetViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        household_config = apps.get_app_config('household')
        self.service = household_config.asset_service



    def list(self, request):
        """Повертає активи для селекту на сторінці створення чека."""
        assets=self.service.get_user_assets(user_id=request.user.id)
        serializer=AssetSerializer(assets,many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer =AssetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        dto=CreateAssetDTO(
            name=serializer.validated_data['name'],
            group_id=serializer.validated_data['group'],
            user_id=request.user.id,
            address_line=serializer.validated_data.get('address_line')
        )

        data=self.service.create(dto)      

        return Response({'id':data.id, 'name':data.name},status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass