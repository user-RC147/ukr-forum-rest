from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
 
from drf_spectacular.utils import extend_schema

from apps.household.api.serializers.asset_serializer import AssetListFilterSerializer, AssetOutSerializer, CreateAssetSerializer
from apps.household.dto.asset_dto import CreateAssetDTO, ListAssetDTO
from apps.household.services.asset_service import AssetService

from apps.household.dto.location_dto import LocationIdInDTO


class AssetViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._service = AssetService()


    #@extend_schema(request=AssetListFilterSerializer, responses=AssetListFilterSerializer)
    def list(self, request):
        """
        GET /api/household/assets/?group=5
        Повертає активи для селекту на сторінці створення чека.
        """
      
        serializer = AssetListFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
       

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        dto = ListAssetDTO(
            group_id=serializer.validated_data.get('group_id'),
        )
            
        asset_list = self._service.get_list_asset(dto,request.user.id)
        
        output_serializer = AssetOutSerializer(asset_list, many=True)
        
        return Response({'results': output_serializer.data}, status=status.HTTP_200_OK)
            
        
    @extend_schema(request=CreateAssetSerializer, responses=AssetOutSerializer)
    def create(self, request):
        creator_user_id = request.user.id
        serializer =CreateAssetSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        dto=CreateAssetDTO(
            name=serializer.validated_data['name'],
            group_id=serializer.validated_data['group_id'],
            #location=LocationInDTO(**location_data),  # Автоматично розпакує country_id, region_id, city_id
            location=LocationIdInDTO(
                country_id=serializer.validated_data['location']['country_id'],
                region_id=serializer.validated_data['location']['region_id'],
                city_id=serializer.validated_data['location']['city_id']
            ),
            address_line=serializer.validated_data.get('address_line')
        )

        data=self._service.create(dto=dto,creator_user_id=creator_user_id)      

        return Response(status=status.HTTP_201_CREATED) #{'id':data.id, 'name':data.name},

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass