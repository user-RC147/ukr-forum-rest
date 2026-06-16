from jsonschema import ValidationError
from rest_framework import serializers


from rest_framework import serializers

class MarketLocationSerializer(serializers.Serializer):
    """Вкладений серіалізатор для красивого групування локації"""
    country_id = serializers.CharField(source='country_name', allow_null=True)
    region_id = serializers.CharField(source='region_name', allow_null=True)
    city_id = serializers.CharField(source='city_name', allow_null=True)


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=150)
    address_line = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    
    # Використовуємо StringRelatedField або ReadOnlyField для відображення юзера у вигляді рядка (username)
    created_by = serializers.CharField(source='created_by.username', default=None, allow_null=True)
    
    # Створюємо динамічне поле для вкладеної локації
    location = serializers.SerializerMethodField()

    def get_location(self, obj):
        """
        Цей метод бере поточний об'єкт магазину і загортає його 
        динамічні поля у вкладений серіалізатор MarketLocationSerializer
        """
        return MarketLocationSerializer(obj).data


# class MarketSerializer(serializers.Serializer):

#     """
#     Серіалізатор магазину.
#     - Магазин глобальний — всі користувачі бачать однакові магазини.
#     - created_by підставляється автоматично з request.user.
#     - Локація повертається як id — резолвиться фронтом через /api/geo/resolve/.
#     """

#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(read_only=True)
#     address_line=serializers.CharField(max_length=255, allow_null=True, allow_blank=True)

#     created_by=serializers.StringRelatedField(read_only=True)


#     country_id=serializers.IntegerField(read_only=True)
#     region_id=serializers.IntegerField(read_only=True)
#     city_id=serializers.IntegerField(read_only=True)

#     # Динамічні текстові поля, які додав сервіс через контракт модулів
#     country_name = serializers.CharField(max_length=100, allow_null=True, required=False)
#     region_name = serializers.CharField(max_length=100, allow_null=True, required=False)
#     city_name = serializers.CharField(max_length=100, allow_null=True, required=False)


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

