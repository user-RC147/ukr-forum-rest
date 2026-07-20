from itertools import product
from rest_framework import serializers

from apps.household.api.serializers.group_serializer import GroupOutSerializer


from apps.household.api.serializers import (
    AssetOutSerializer,
    MarketSerializer,
    ProductOutSerializer,
)


class PurchaseItemOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = ProductOutSerializer()
    quantity = serializers.DecimalField(max_digits=12,decimal_places=3)
    price_per_unit=serializers.DecimalField(max_digits=12, decimal_places=2)


class PurchaseOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    asset = AssetOutSerializer()
    market = MarketSerializer()
    data_purchase = serializers.DateField()
    note = serializers.CharField()
    created_by_id=serializers.IntegerField()
    created_at = serializers.DateTimeField()
    items = list[PurchaseItemOutSerializer()]


class CreatePurchaseItemSerializer(serializers.Serializer):
    """
    Валідатор для одного рядка товару всередині чека.
    """

    product_id = serializers.IntegerField()
    quantity = serializers.DecimalField(
        max_digits=8,
        decimal_places=3,
        help_text="Кількість товару (наприклад, 1.500 або 3.000)",
    )
    price_per_unit = serializers.DecimalField(
        max_digits=6, decimal_places=2, help_text="Ціна за одиницю товару"
    )


class CreatePurchaseSerializer(serializers.Serializer):
    """
    Головний валідатор для всієї форми створення чека.
    """

    asset_id = serializers.IntegerField(
        help_text="ID об'єкта, до якого прив'язуються витрати"
    )
    market_id = serializers.IntegerField(help_text="ID магазину (обов'язкове поле)")
    # group_id = GroupOutSerializer()

    data_purchase = serializers.DateTimeField(help_text="Дата здійснення покупки")
    # note = serializers.CharField(
    #     required=False,
    #     allow_blank=True,
    #     default="",
    #     help_text="Додаткова текстова нотатка до чека",
    # )

    # Вкладений серіалізатор для перевірки списку товарів (таблиці)
    items = CreatePurchaseItemSerializer()
