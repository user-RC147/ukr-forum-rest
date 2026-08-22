from rest_framework import serializers

from core.serializers.location_serializer import LocationInSerializer,LocationOutSerializer

class CountryOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    code=serializers.CharField()
    flag_emoji=serializers.CharField()
    currency=serializers.CharField()


class RegionOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    country_id=serializers.IntegerField()

class CityOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    region_id = serializers.IntegerField()
    country_id = serializers.IntegerField() 
    latitude=serializers.DecimalField(max_digits=20, decimal_places=16)
    longitude=serializers.DecimalField(max_digits=20, decimal_places=16)
