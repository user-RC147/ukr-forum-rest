from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    country_id = serializers.IntegerField()
    region_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    files = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True),
        allow_empty=True,
        max_length=10,
    )


class ProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    owner_id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M:%S")
    country = serializers.DictField()
    region = serializers.DictField()
    city = serializers.DictField()
    category = serializers.DictField()
    files = serializers.ListField(child=serializers.DictField(), default=list)
