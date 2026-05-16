from rest_framework import viewsets
from .serializers import ProductSerializer
from .service import ProductService
from rest_framework.response import Response
from rest_framework import status
from apps.shop.exceptions import ProductNotFound, UnauthorizedException
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ViewSet):
    lookup_value_regex = r"\d+"

    serializer_class = ProductSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_permissions(self):
        if self.action in ["create", "destroy", "partial_update"]:
            return [IsAuthenticated()]
        return []

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 400 if not valid

        product = self.service.create(
            user_id=request.user.id, data=serializer.validated_data
        )

        return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            product = self.service.get(pk)
        except ProductNotFound as e:
            raise NotFound(detail=str(e))

        serializer = ProductSerializer(product)

        return Response(serializer.data)

    def partial_update(self, request, pk):
        try:
            product = self.service.get(pk)
        except ProductNotFound as e:
            raise NotFound(detail=str(e))

        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            product = self.service.update(
                id=pk, user_id=request.user.id, data=serializer.validated_data
            )
        except UnauthorizedException:
            raise PermissionDenied(detail="Access denied")

        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

    def list(self, request):
        product = self.service.get_all()

        serializer = ProductSerializer(product, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            self.service.delete(pk, user_id=request.user.id)
        except ProductNotFound as e:
            raise NotFound(detail=str(e))
        except UnauthorizedException:
            raise PermissionDenied(detail="Access denied")

        return Response(status=status.HTTP_204_NO_CONTENT)
