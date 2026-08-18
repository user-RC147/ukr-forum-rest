from rest_framework import serializers


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    code = serializers.CharField()
    flag_emoji = serializers.CharField()
    currency = serializers.CharField()


class CountrySearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=True)
