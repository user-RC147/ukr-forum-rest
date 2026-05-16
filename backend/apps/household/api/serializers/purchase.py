from rest_framework import serializers

from apps.household.models import Purchase,PurchaseItem
from apps.users.services.user_service import user_service


class PurchaseItemSerializer(serializers.ModelSerializer):

    """
    Серіалізатор рядка чеку.
    - total_price — обчислюється автоматично через @property.
    - product_name_snapshot — заповнюється автоматично в моделі через save().
    """

    total_price =serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
    )


    class Meta:
        model=PurchaseItem
        fields=[
            'id',
            'product',
            'product_name_snapshot',
            'quantity',
            'price_per_unit',
            'total_price',
        ]
        read_only_fields=['id','product_name_snapshot','total_price']


class PurchaseSerializer(serializers.ModelSerializer):

    """
    Серіалізатор чеку з вкладеними рядками.
    - items — вкладений список рядків чеку.
    - total_amount — сума всіх рядків, обчислюється через @property.
    - created_by — підставляється автоматично з request.user.
    """

    items=PurchaseItemSerializer(many=True)
    total_amount= serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,        
    )
    
    created_by = serializers.SerializerMethodField()
    
    class Meta:
        model=Purchase
        fields=[
            'id',
            'asset',
            'market',
            'created_by',
            'data_purchase',
            'note',
            'created_at',
            'total_amount',
            'items',
        ]
        read_only_fields=['id','created_by','created_at','total_amount']

    def get_created_by(self,obj):
        """
        Повертає дані користувача через UserDTO.
        users модуль не імпортується напряму — тільки через сервіс.
        """
        if not obj.created_by_id:
            return None
        dto=user_service.get_user(obj.created_by_id)
        if not dto:
            return None
        return {
            'id':dto.id,
            'username':dto.username,
            'display_name':dto.display_name,
        }

    def create(self,validated_data):
        # витягуємо items окремо — вони не передаються напряму в Purchase
        items_data=validated_data.pop('items')

        # створюємо чек
        purchase=Purchase.objects.create(**validated_data)

        # створюємо рядки чеку
        # один запит замість N
        items = []
        for item_data in items_data:
            product = item_data.get('product')
            if product:
                item_data['product_name_snapshot'] = product.name
            items.append(PurchaseItem(purchase=purchase, **item_data))

        PurchaseItem.objects.bulk_create(items)

        return purchase
    

    def update(self,instance,validated_data):
        items_data=validated_data.pop('items',None)

        # оновлюємо поля чеку
        for attr, value in validated_data.items():
            setattr(instance,attr,value)
        instance.save()

        # якщо items передані — видаляємо старі і створюємо нові
        if items_data is not None:
            instance.items.all().delete()

            items = []
            for item_data in items_data:
                product = item_data.get('product')
                if product:
                    item_data['product_name_snapshot'] = product.name
                items.append(PurchaseItem(purchase=instance, **item_data))

            PurchaseItem.objects.bulk_create(items)
            
        return instance