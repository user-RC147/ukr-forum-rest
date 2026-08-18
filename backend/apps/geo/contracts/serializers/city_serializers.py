from rest_framework import serializers

from .region_serializers import RegionSerializer


class CitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    region = RegionSerializer()
    country_id = serializers.IntegerField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
