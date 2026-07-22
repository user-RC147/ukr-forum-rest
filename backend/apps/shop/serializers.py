from rest_framework import serializers

from .enums import PRODUCT_STATUS_LABELS, ProductStatus


class ProductSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    country_id = serializers.IntegerField()
    region_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    category_id = serializers.IntegerField()
    status = serializers.ChoiceField(
        choices=[(s.value, PRODUCT_STATUS_LABELS[s]) for s in ProductStatus]
    )
    files = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True),
        allow_empty=True,
        max_length=10,
    )


class ProductUpdateSerializer(ProductSerializer):
    files = None

    update_file_ids = serializers.ListField(
        child=serializers.IntegerField(), max_length=10
    )
    update_files = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), max_length=10
    )
    create_files = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), max_length=10
    )
    keep_files_ids = serializers.ListField(
        child=serializers.IntegerField(), max_length=10
    )


class ProductReadSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    owner = serializers.DictField()
    title = serializers.CharField()
    description = serializers.CharField()
    price = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    status = serializers.ChoiceField(
        choices=[(s.value, PRODUCT_STATUS_LABELS[s]) for s in ProductStatus]
    )
    country = serializers.DictField()
    region = serializers.DictField()
    city = serializers.DictField()
    category = serializers.DictField()
    files = serializers.ListField(child=serializers.DictField(), default=list)


class ProductListQuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
