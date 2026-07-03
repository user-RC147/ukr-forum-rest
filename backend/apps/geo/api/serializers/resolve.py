from rest_framework import serializers


class CountrySerializer(serializers.Serializer):

    """Серіалізатор країни для resolve відповіді."""
    
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    code=serializers.CharField()
    flag_emoji=serializers.CharField()
    currency=serializers.CharField()


class RegionSerializer(serializers.Serializer):
    """Серіалізатор регіону для resolve відповіді."""
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()


class CitySerializer(serializers.Serializer):
    """Серіалізатор міста для resolve відповіді."""
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    region = serializers.DictField()
    country_id = serializers.IntegerField()