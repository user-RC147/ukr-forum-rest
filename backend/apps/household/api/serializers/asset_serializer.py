from rest_framework import serializers

from apps.household.api.serializers.group_serializer import GroupOutSerializer
from apps.household.api.serializers.location_serializer import LocationInSerializer, LocationOutSerializer
from apps.household.dto.group_dto import GroupOutDTO

from core.serializers.location_serializer import Location_id_region_OutSerializer

class AssetOutSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)    
    group = GroupOutSerializer(read_only=True)  # ← для читання
    location=LocationOutSerializer(read_only=True)
    address_line = serializers.CharField(required=False, allow_null=True)

class AssetIdRegionOutSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)    
    group = GroupOutSerializer(read_only=True)  # ← для читання
    location=Location_id_region_OutSerializer(read_only=True)
    address_line = serializers.CharField(required=False, allow_null=True)



class CreateAssetSerializer(serializers.Serializer):
    name=serializers.CharField()
    group_id=serializers.IntegerField(read_only=True)
    #location=LocationInSerializer()
    country_id=serializers.IntegerField(read_only=True)
    region_id=serializers.IntegerField(read_only=True)
    city_id=serializers.IntegerField(read_only=True)
    address_line=serializers.CharField()




class AssetListFilterSerializer(serializers.Serializer):
    # Тепер параметр можна не передавати
    group_id = serializers.IntegerField(required=False, allow_null=True)