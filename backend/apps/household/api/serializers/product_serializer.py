from rest_framework import serializers
from apps.household.api.serializers.unit_of_measure_serializer import UnitOfMeasureSerializer


class CategoryProductSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=100)
    is_active=serializers.BooleanField(read_only=True)

class ProductInSerializer(serializers.Serializer):

    """
    Серіалізатор товару.
    - Товар глобальний — всі користувачі бачать однакові товари.
    - category повертається як id.
    - created_by підставляється автоматично з request.user.
    """
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=150)
    unit_of_measure_id=serializers.IntegerField()
    category_id=serializers.IntegerField(required=False,allow_null=True)


class ProductOutSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(max_length=150)
    unit_of_measure='UnitOfMeasureSerializer'
    category='CategoryProductSerializer'
    #created_by=''


class CreateProductSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=150)
    unit_of_measure_id=serializers.IntegerField()
    category_id=serializers.IntegerField(required=False,allow_null=True)
    created_by_id=serializers.IntegerField()