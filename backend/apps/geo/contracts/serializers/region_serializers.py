from rest_framework import serializers


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    country_id = serializers.IntegerField()
