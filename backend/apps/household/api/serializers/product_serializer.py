from rest_framework import serializers


class ProductSerializer(serializers.Serializer):

    """
    Серіалізатор товару.
    - Товар глобальний — всі користувачі бачать однакові товари.
    - category повертається як id.
    - created_by підставляється автоматично з request.user.
    """
    id=serializers.ImageField(read_only=True)
    name=serializers.CharField(max_length=150)
    unit_of_measure=serializers.CharField(max_length=10,default='шт.')
    category_id=serializers.IntegerField(required=False,allow_null=True)