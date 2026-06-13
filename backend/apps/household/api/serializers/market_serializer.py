from jsonschema import ValidationError
from rest_framework import serializers



class MarketSerializer(serializers.Serializer):

    """
    Серіалізатор магазину.
    - Магазин глобальний — всі користувачі бачать однакові магазини.
    - created_by підставляється автоматично з request.user.
    - Локація повертається як id — резолвиться фронтом через /api/geo/resolve/.
    """

    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(read_only=True)
    address_line=serializers.CharField(read_only=True)

    created_by=serializers.StringRelatedField(read_only=True)


    country_id=serializers.IntegerField(read_only=True)
    region_id=serializers.IntegerField(read_only=True)
    city_id=serializers.IntegerField(read_only=True)


class MarketCreateSerializer(serializers.Serializer):
    """
    Серіалізатор для створення/оновлення об'єкта з гнучкою локацією.
    Проводить первинну валідацію типів даних.
    """
    name =serializers.CharField(max_length=255,required=True)
    address_line=serializers.CharField(max_length=255,required=False, allow_blank=True)

    # Робимо поля локації необов'язковими (allow_null=True), 
    # щоб користувач міг обрати лише країну або країну + регіон.
    country_id =serializers.IntegerField(required=False,allow_null=True,default=None)
    region_id=serializers.IntegerField(required=False,allow_null=True,default=None)
    city_id=serializers.IntegerField(required=False,allow_null=True,default=None)

    def validate(self,attrs):
        """
        Тут ми можемо перевірити бізнес-логіку зв'язків.
        Наприклад: якщо вказано місто, але не вказано регіон — це помилка валідації.
        """
        country_id=attrs.get('country_id')
        region_id=attrs.get('region_id')
        city_id=attrs.get('city_id')

        if region_id and not country_id:
            raise serializers.ValidationError(
                {"region_id": "Не можна вказати регіон без вказання країни."}
            )
        
        if city_id and not region_id:
            raise serializers.ValidationError(
                {"city_id": "Не можна вказати місто без вказання регіону."}
            )

        return attrs

