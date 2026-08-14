from rest_framework import serializers


class CountrySerializer(serializers.Serializer):
    """Серіалізатор країни для resolve відповіді."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    code = serializers.CharField()
    flag_emoji = serializers.CharField()
    currency = serializers.CharField()


class RegionSerializer(serializers.Serializer):
    """Серіалізатор регіону для resolve відповіді."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    country_id = serializers.IntegerField()


class CitySerializer(serializers.Serializer):
    """Серіалізатор міста для resolve відповіді."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    region = RegionSerializer()
    country_id = serializers.IntegerField()


class CityQuerySerializer(serializers.Serializer):
    region_id = serializers.IntegerField(required=True)


class RegionQuerySerializer(serializers.Serializer):
    country_id = serializers.IntegerField(required=True)


class SearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=True)


class CitySearchQuerySerializer(SearchQuerySerializer):
    country_id = serializers.IntegerField(required=True)
