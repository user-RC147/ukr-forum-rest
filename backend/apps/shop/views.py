from rest_framework import viewsets
from .serializers import ProductSerializer
from .service import ProductService
from rest_framework.response import Response
from rest_framework import status

# Create your views here.



class ProductViewSet(viewsets.ViewSet):
    lookup_value_regex = r'\d+'

    serializer_class = ProductSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400 if not valid
        
        product = self.service.create(data=serializer.validated_data)
        
        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        product = self.service.get(pk)

        serializer = ProductSerializer(product)

        return Response(serializer.data)
    
    def partial_update(self, request, pk):
        product = self.service.get(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        product = self.service.update(id=pk, data=serializer.validated_data)

        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
    
    def list(self, request):
        product = self.service.get_all()

        serializer = ProductSerializer(product, many=True)

        return Response(serializer.data)
    
    def destroy(self, request, pk=None):

        self.service.delete(pk)
        
        return Response({"id": pk, "deleted": True}, status=status.HTTP_200_OK)