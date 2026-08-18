from rest_framework import serializers


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    country_id = serializers.IntegerField()


class RegionQuerySerializer(serializers.Serializer):
    country_id = serializers.IntegerField(required=True)
