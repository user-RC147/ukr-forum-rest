from rest_framework import serializers

from apps.household.models import Market

class MarketSerializer(serializers.ModelSerializer):

    """
    Серіалізатор магазину.
    - Магазин глобальний — всі користувачі бачать однакові магазини.
    - created_by підставляється автоматично з request.user.
    - Локація повертається як id — резолвиться фронтом через /api/geo/resolve/.
    """

    created_by=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Market
        fields=[
            'id','name','address_line','country_id','region_id','city_id','created_by'
        ]
        read_only_fields=['id','created_by']