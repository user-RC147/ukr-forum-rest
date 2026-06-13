from rest_framework import serializers

from apps.household.models import Product

class ProductSerializer(serializers.ModelSerializer):

    """
    Серіалізатор товару.
    - Товар глобальний — всі користувачі бачать однакові товари.
    - category повертається як id.
    - created_by підставляється автоматично з request.user.
    """

    created_by=serializers.StringRelatedField(read_only=True)
    category_name=serializers.CharField(source='category.name',read_only=True)

    class Meta:
        model=Product
        fields=[
            'id',
            'name',
            'unit_of_measure',
            'category',
            'category_name',
            'created_by',
        ]
        read_only_fields=['id','created_by','category_name']