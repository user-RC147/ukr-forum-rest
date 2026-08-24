
from rest_framework import serializers

from apps.household.api.serializers.location_serializer import LocationInSerializer, LocationOutSerializer
from core.serializers.location_serializer import Location_id_region_OutSerializer




class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    code = serializers.CharField()
    flag_emoji = serializers.CharField()
    currency = serializers.CharField()


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    name_ua = serializers.CharField()
    country_id = serializers.IntegerField()


class CitySerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    country_id=serializers.IntegerField()
    region_id=serializers.IntegerField()
    latitude=serializers.DecimalField(max_digits=10,decimal_places=8)
    longitude=serializers.DecimalField(max_digits=10,decimal_places=8)


class MarketLocationSerializer(serializers.Serializer):
    """Вкладений серіалізатор для красивого групування локації"""

    country = CountrySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    city = CitySerializer(read_only=True)



class MarketExpenseInSerializer(serializers.Serializer):
    id =serializers.IntegerField()

class MarketExpense_Id_OutSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    name=serializers.CharField()
    location=Location_id_region_OutSerializer()
    address_line=serializers.CharField()
    total = serializers.DecimalField(max_digits=12,decimal_places=3)

class MarketExpenseOutSerializer(serializers.Serializer):
    id =serializers.IntegerField()
    name=serializers.CharField()
    location=LocationOutSerializer()
    address_line=serializers.CharField()
    total = serializers.DecimalField(max_digits=12,decimal_places=3)


class MarketSerializer(serializers.Serializer):
    """
    Серіалізатор магазину.
    - Магазин глобальний — всі користувачі бачать однакові магазини.
    - created_by підставляється автоматично з request.user.
    - Локація повертається як id — резолвиться фронтом через /api/geo/resolve/.
    """

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address_line = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True
    )

    created_by = serializers.StringRelatedField(read_only=True)

    country_id = serializers.IntegerField(read_only=True)
    region_id = serializers.IntegerField(read_only=True)
    city_id = serializers.IntegerField(read_only=True)

    # Динамічні текстові поля, які додав сервіс через контракт модулів
    country_name = serializers.CharField(
        max_length=100, allow_null=True, required=False
    )
    region_name = serializers.CharField(max_length=100, allow_null=True, required=False)
    city_name = serializers.CharField(max_length=100, allow_null=True, required=False)


class MarketFullSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address_line = serializers.CharField(
        max_length=255, allow_null=True, allow_blank=True
    )

    created_by = serializers.StringRelatedField(read_only=True)

    location = Location_id_region_OutSerializer(read_only=True)


class MarketCreateSerializer(serializers.Serializer):
    """
    Серіалізатор для створення/оновлення об'єкта з гнучкою локацією.
    Проводить первинну валідацію типів даних.
    """

    name = serializers.CharField(max_length=255, required=True)
    address_line = serializers.CharField(
        max_length=255, required=False, allow_blank=True
    )

    # Робимо поля локації необов'язковими (allow_null=True),
    # щоб користувач міг обрати лише країну або країну + регіон.
    country_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    region_id = serializers.IntegerField(required=False, allow_null=True, default=None)
    city_id = serializers.IntegerField(required=False, allow_null=True, default=None)

    def validate(self, attrs):
        """
        Тут ми можемо перевірити бізнес-логіку зв'язків.
        Наприклад: якщо вказано місто, але не вказано регіон — це помилка валідації.
        """
        country_id = attrs.get("country_id")
        region_id = attrs.get("region_id")
        city_id = attrs.get("city_id")

        if region_id and not country_id:
            raise serializers.ValidationError(
                {"region_id": "Не можна вказати регіон без вказання країни."}
            )

        if city_id and not region_id:
            raise serializers.ValidationError(
                {"city_id": "Не можна вказати місто без вказання регіону."}
            )

        return attrs


