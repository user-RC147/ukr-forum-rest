from rest_framework import serializers


class PaginatorSerializerOut(serializers.Serializer):

    
    #items=PurchaseItemOutSerializer(many=True)    # самі дані сторінки
    count=serializers.IntegerField()          # загальна кількість елементів (всього, без урахування сторінки)
    page=serializers.IntegerField()             # поточна сторінка
    page_size=serializers.IntegerField()        # розмір сторінки
    total_pages=serializers.IntegerField()       # загальна кількість сторінок
    has_next=serializers.BooleanField()        # чи є наступна сторінка
    has_previous=serializers.BooleanField()