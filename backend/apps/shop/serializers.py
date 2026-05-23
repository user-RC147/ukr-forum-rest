from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    country_id = serializers.IntegerField()
    region_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
