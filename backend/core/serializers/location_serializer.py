from rest_framework import serializers

from apps.geo.api.serializers import CountrySerializer,RegionSerializer,CitySerializer


class LocationOutSerializer(serializers.Serializer):
    country=CountrySerializer()
    region=RegionSerializer()
    city=CitySerializer()

class LocationInSerializer(serializers.Serializer):
    country_id=serializers.IntegerField()
    region_id=serializers.IntegerField()
    city_id=serializers.IntegerField()