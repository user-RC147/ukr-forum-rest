import dataclasses
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.files import exceptions as files_exceptions
from apps.search.contracts import exceptions as search_exceptions
from apps.shop.exceptions import GeoNotFound, NotFoundError, ProductPermissionError
from apps.shop.schemas import product_create_schema, product_update_schema
from .dto import ProductCreateDTO, ProductUpdateDTO

from .serializers import ProductReadSerializer, ProductSerializer, ProductUpdateSerializer
from .service import ProductService


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

    @product_create_schema
    def create(self, request):
        data = request.data.dict()
        data["files"] = request.FILES.getlist("files")
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)  # 400 if not valid

        data = _to_dto_create(request.user.id, serializer.validated_data)
        try:
            product = self.service.create(data)
        except GeoNotFound as e:
            raise NotFound(detail=str(e))

        return Response(
            ProductReadSerializer(product).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk: int):
        try:
            product = self.service.get(pk)
        except (
            files_exceptions.NotFoundError,
            search_exceptions.NotFoundError,
            NotFoundError,
        ) as e:
            raise NotFound(detail=str(e))

        serializer = ProductReadSerializer(product)

        return Response(serializer.data)

    @product_update_schema
    def partial_update(self, request, pk: int):

        serializer = ProductUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = _to_dto_update(pk, serializer.validated_data)

        try:
            product = self.service.update(request.user.id, data)
        except ProductPermissionError:
            raise PermissionDenied(detail="Access denied")
        except files_exceptions.NotFoundError as e:
            raise NotFound(detail=str(e))
        except files_exceptions.ValidationError as e:
            raise ValidationError(detail=str(e))

        return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)

    def list(self, request):
        product = self.service.get_all()

        serializer = ProductReadSerializer(product, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            self.service.delete(pk, user_id=request.user.id)
        except (
            files_exceptions.NotFoundError,
            search_exceptions.NotFoundError,
            NotFoundError,
        ) as e:
            raise NotFound(detail=str(e))
        except ProductPermissionError:
            raise PermissionDenied(detail="Access denied")

        return Response(status=status.HTTP_204_NO_CONTENT)


def _to_dto_create(owner_id: int, data) -> ProductCreateDTO:
    return ProductCreateDTO(
        title=data["title"],
        owner_id=owner_id,
        description=data["description"],
        country_id=data["country_id"],
        region_id=data["region_id"],
        city_id=data["city_id"],
        category_id=data["category_id"],
        price=data["price"],
        files=data["files"],
    )

def _to_dto_update(id: int, data) -> ProductUpdateDTO:
    allowed = {f.name for f in dataclasses.fields(ProductUpdateDTO)} - {"id"}
    kwargs = {k: v for k, v in data.items() if k in allowed}
    return ProductUpdateDTO(id=id, **kwargs)
