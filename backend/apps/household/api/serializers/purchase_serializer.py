from rest_framework import serializers

from apps.household.dto.purchase_dto import CreatePurchaseInDTO, PurchaseItemInDTO


class PurchaseItemCreateSerializer(serializers.Serializer):
    """
    Валідатор для одного рядка товару всередині чека.
    """

    product_id = serializers.IntegerField(help_text="ID товару з глобального довідника")
    quantity = serializers.DecimalField(
        max_digits=12,
        decimal_places=3,
        help_text="Кількість товару (наприклад, 1.500 або 3.000)",
    )
    price_per_unit = serializers.DecimalField(
        max_digits=12, decimal_places=2, help_text="Ціна за одиницю товару"
    )


class PurchaseCreateSerializer(serializers.Serializer):
    """
    Головний валідатор для всієї форми створення чека.
    """

    asset_id = serializers.IntegerField(
        help_text="ID об'єкта, до якого прив'язуються витрати"
    )
    market_id = serializers.IntegerField(help_text="ID магазину (обов'язкове поле)")
    data_purchase = serializers.DateField(help_text="Дата здійснення покупки")
    note = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        help_text="Додаткова текстова нотатка до чека",
    )

    # Вкладений серіалізатор для перевірки списку товарів (таблиці)
    items = PurchaseItemCreateSerializer(
        many=True, allow_empty=False, help_text="Список куплених товарів у чеку"
    )

    def to_dto(self) -> CreatePurchaseInDTO:
        """
        Конвертує перевірені дані серіалізатора (validated_data)
        у строге та чисте DTO для передачі в сервіс.
        """
        data = self.validated_data

        # 1. Спочатку згортаємо всі рядки товарів у список DTO товарів
        items_dto = [
            PurchaseItemInDTO(
                product_id=item["product_id"],
                quantity=item["quantity"],
                price_per_unit=item["price_per_unit"],
            )
            for item in data["items"]
        ]

        # 2. Повертаємо головне DTO чека, куди вкладаємо список товарів
        to_dto_items = CreatePurchaseInDTO(
            asset_id=data["asset_id"],
            market_id=data["market_id"],
            data_purchase=data["data_purchase"],
            note=data.get("note", ""),
            items=items_dto,
        )

        return to_dto_items








# class PurchaseItemSerializer(serializers.ModelSerializer):

#     """
#     Серіалізатор рядка чеку.
#     - total_price — обчислюється автоматично через @property.
#     - product_name_snapshot — заповнюється автоматично в моделі через save().
#     """

#     total_price =serializers.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         read_only=True,
#     )


#     class Meta:
#         model=PurchaseItem
#         fields=[
#             'id',
#             'product',
#             'product_name_snapshot',
#             'quantity',
#             'price_per_unit',
#             'total_price',
#         ]
#         read_only_fields=['id','product_name_snapshot','total_price']


# class PurchaseSerializer(serializers.ModelSerializer):

#     """
#     Серіалізатор чеку з вкладеними рядками.
#     - items — вкладений список рядків чеку.
#     - total_amount — сума всіх рядків, обчислюється через @property.
#     - created_by — підставляється автоматично з request.user.
#     """

#     items=PurchaseItemSerializer(many=True)
#     total_amount= serializers.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         read_only=True,
#     )

#     created_by = serializers.SerializerMethodField()

#     class Meta:
#         model=Purchase
#         fields=[
#             'id',
#             'asset',
#             'market',
#             'created_by',
#             'data_purchase',
#             'note',
#             'created_at',
#             'total_amount',
#             'items',
#         ]
#         read_only_fields=['id','created_by','created_at','total_amount']

#     def get_created_by(self,obj):
#         """
#         Повертає дані користувача через UserDTO.
#         users модуль не імпортується напряму — тільки через сервіс.
#         """
#         if not obj.created_by_id:
#             return None
#         dto=user_service.get_user(obj.created_by_id)
#         if not dto:
#             return None
#         return {
#             'id':dto.id,
#             'username':dto.username,
#             'display_name':dto.display_name,
#         }

#     def create(self,validated_data):
#         # витягуємо items окремо — вони не передаються напряму в Purchase
#         items_data=validated_data.pop('items')

#         # створюємо чек
#         purchase=Purchase.objects.create(**validated_data)

#         # створюємо рядки чеку
#         # один запит замість N
#         items = []
#         for item_data in items_data:
#             product = item_data.get('product')
#             if product:
#                 item_data['product_name_snapshot'] = product.name
#             items.append(PurchaseItem(purchase=purchase, **item_data))

#         PurchaseItem.objects.bulk_create(items)

#         return purchase


#     def update(self,instance,validated_data):
#         items_data=validated_data.pop('items',None)

#         # оновлюємо поля чеку
#         for attr, value in validated_data.items():
#             setattr(instance,attr,value)
#         instance.save()

#         # якщо items передані — видаляємо старі і створюємо нові
#         if items_data is not None:
#             instance.items.all().delete()

#             items = []
#             for item_data in items_data:
#                 product = item_data.get('product')
#                 if product:
#                     item_data['product_name_snapshot'] = product.name
#                 items.append(PurchaseItem(purchase=instance, **item_data))

#             PurchaseItem.objects.bulk_create(items)

#         return instance
