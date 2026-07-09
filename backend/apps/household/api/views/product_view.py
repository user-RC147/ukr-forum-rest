from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from drf_spectacular.utils import extend_schema

from apps.household.api.serializers.product_serializer import CreateProductSerializer, ProductInSerializer,ProductOutSerializer
from apps.household.dto.product_dto import CreateProductInDTO,ProductOutDTO
from apps.household.services.product_service import ProductService

from apps.users.exceptions import UserNotFoundException
from apps.household.exceptions import ProductAlreadyExistsException

import logging

logger = logging.getLogger(__name__)


class ProductViewSet(ViewSet):
    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._service = ProductService()
    

    def list(self, request):
        products=self._service.get_all_products()

        serializer=ProductOutSerializer(products,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)


    @extend_schema(request=CreateProductSerializer, responses=CreateProductSerializer)
    def create(self, request):

        data = request.data
        
        data['created_by_id']=request.user.id


        serializer=CreateProductSerializer(data=data)
        

        #group_in_user_exsits = self._service.
        
        
        if serializer.is_valid():
            data=serializer.validated_data

            dto = CreateProductInDTO(
                name=data['name'],
                unit_of_measure_id=data['unit_of_measure_id'],
                category_id=data.get("category_id") or None
                
            )  # Конвертуємо словник у DTO
            try:
                product=self._service.create(dto=dto,user_id=user_id)

            except UserNotFoundException as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ProductAlreadyExistsException as e:
                return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)  
            return Response(ProductOutSerializer(product).data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass