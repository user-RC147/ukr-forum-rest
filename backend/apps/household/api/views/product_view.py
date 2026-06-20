from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.apps import apps

from apps.household.apps import HouseholdConfig
from apps.household.api.serializers.product_serializer import ProductSerializer
from apps.household.dto.product_dto import CreateProductInDTO


class ProductViewSet(ViewSet):
    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.service=HouseholdConfig.product_service

         # 2. Дістаємо поточний ініціалізований екземпляр додатка з контейнера Django
        household_app = apps.get_app_config('household')
        
        # 3. Тепер @property відпрацює правильно і поверне готовий ....  
        self.service = household_app.product_service 
    

    def list(self, request):
        """GET /api/household/products/?search=хліб"""
        products=self.service.get_all_products(search_query=None)
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass