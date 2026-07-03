from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.household.api.serializers.product_serializer import ProductSerializer
from apps.household.dto.product_dto import CreateProductInDTO
from apps.household.services.product_service import ProductService

from apps.users.exceptions import UserNotFoundException
from apps.household.exceptions import ProductAlreadyExistsException


class ProductViewSet(ViewSet):
    permission_classes=[IsAuthenticated]

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._service = ProductService()
    

    def list(self, request):
        """GET /api/household/products/?search=хліб"""

        search_query=request.query_params.get('search',None)

        products=self._service.get_all_products(search_query=search_query)

        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)




    def create(self, request):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            data=serializer.validated_data
            dto = CreateProductInDTO(
                name=data['name'],
                unit_of_measure=data['unit_of_measure'],
                created_by=request.user.id
            )  # Конвертуємо словник у DTO
            try:
                product=self._service.create(dto,request.user)
            except UserNotFoundException as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ProductAlreadyExistsException as e:
                return Response({"error": str(e)}, status=status.HTTP_409_CONFLICT)  
            return Response(ProductSerializer(product).data,status=status.HTTP_201_CREATED)
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