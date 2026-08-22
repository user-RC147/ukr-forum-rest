from rest_framework import serializers

from apps.geo.contracts.serializers import CountrySerializer ,RegionSerializer,CitySerializer




#==========================================================

class City_id_region_Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    region_id = serializers.IntegerField()
    country_id = serializers.IntegerField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)


class Location_id_region_OutSerializer(serializers.Serializer):
    country=CountrySerializer()
    region=RegionSerializer()
    city=City_id_region_Serializer()

#==========================================================

class LocationOutSerializer(serializers.Serializer):
    country=CountrySerializer()
    region=RegionSerializer()
    city=CitySerializer()

class LocationInSerializer(serializers.Serializer):
    country_id=serializers.IntegerField()
    region_id=serializers.IntegerField()
    city_id=serializers.IntegerField()