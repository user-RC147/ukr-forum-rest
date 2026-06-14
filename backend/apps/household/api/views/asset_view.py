import stat
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from rest_framework import status

from apps.household.apps import HouseholdConfig
from apps.household.api.serializers.asset_serializer import AssetListFilterSerializer, AssetSerializer
from apps.household.dto.asset_dto import CreateAssetDTO, ListAssetDTO
from apps.household.services import AssetService
from apps.shop import serializers


class AssetViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        household_config = apps.get_app_config('household')
        self.service = household_config.asset_service



    def list(self, request):
        """
        GET /api/household/assets/?group=5
        Повертає активи для селекту на сторінці створення чека.
        """
        # 1. Беремо group_id з query_params (урл-рядка), а не з тіла запиту
        serializer = AssetListFilterSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Формуємо DTO
        dto = ListAssetDTO(
            group_id=serializer.validated_data.get('group_id'),
            user_id=request.user.id
        )
        
        # 3. Викликаємо бізнес-логику
        asset_list = self.service.get_list_asset(dto)
        
        # 4. ОБОВ'ЯЗКОВО СЕРІАЛІЗУЄМО список моделей перед відповіддю
        # Використовуємо many=True, бо передаємо список об'єктів
        output_serializer = AssetSerializer(asset_list, many=True)
        
        return Response({'results': output_serializer.data}, status=status.HTTP_200_OK)
            
        

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