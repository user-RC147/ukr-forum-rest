import dataclasses
import re

from django.core.files.uploadedfile import UploadedFile
from rest_framework import status, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.shop.schemas import (
    product_create_schema,
    product_list_schema,
    product_update_schema,
)

from .dto import ProductCreateDTO, ProductUpdateDTO, RequestUserDTO
from .serializers import (
    ProductListQuerySerializer,
    ProductReadSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)
from .service import ProductService


class RequiresAuthIfUserIdParam(BasePermission):
    def has_permission(self, request, view):
        if request.query_params.get("user_id"):
            return request.user.is_authenticated
        return True


class ProductViewSet(viewsets.ViewSet):
    lookup_value_regex = r"\d+"

    serializer_class = ProductSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    def get_permissions(self):
        if self.action in ["create", "destroy", "partial_update"]:
            return [IsAuthenticated()]
        elif self.action == "list":
            return [RequiresAuthIfUserIdParam()]
        return []

    @product_create_schema
    def create(self, request):
        data = request.data.dict()
        data["files"] = request.FILES.getlist("files")
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)  # 400 if not valid

        data = _to_dto_create(serializer.validated_data)

        user = _to_dto_user(request.user)

        product = self.service.create(user, data)

        return Response(
            ProductReadSerializer(product).data, status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk: int):
        product = self.service.get(pk)

        serializer = ProductReadSerializer(product)

        return Response(serializer.data)

    @product_update_schema
    def partial_update(self, request, pk: int):

        serializer = ProductUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data["update_files"] = _extract_update_files(request)
        data = _to_dto_update(pk, data)

        user = _to_dto_user(request.user)
        product = self.service.update(user, data)

        return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)

    @product_list_schema
    def list(self, request: Request):
        query = ProductListQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        user_id = query.validated_data.get("user_id")
        if user_id:
            user = _to_dto_user(request.user)
            product = self.service.get_all(user=user, user_id=user_id)
        else:
            product = self.service.get_all()

        serializer = ProductReadSerializer(product, many=True)

        return Response(serializer.data)

    def destroy(self, request, pk: int):
        user = _to_dto_user(request.user)
        self.service.delete(user, pk)

        return Response(status=status.HTTP_204_NO_CONTENT)


def _to_dto_user(user) -> RequestUserDTO:
    return RequestUserDTO(id=user.id, is_staff=user.is_staff)


def _to_dto_create(data) -> ProductCreateDTO:
    return ProductCreateDTO(
        title=data["title"],
        description=data["description"],
        country_id=data["country_id"],
        region_id=data["region_id"],
        city_id=data["city_id"],
        category_id=data["category_id"],
        price=data["price"],
        status=data["status"],
        files=data["files"],
    )


def _to_dto_update(id: int, data) -> ProductUpdateDTO:
    allowed = {f.name for f in dataclasses.fields(ProductUpdateDTO)} - {"id"}
    kwargs = {k: v for k, v in data.items() if k in allowed}
    return ProductUpdateDTO(id=id, **kwargs)


UPDATE_FILE_KEY_RE = re.compile(r"^update_files\[(\d+)\]$")


def _extract_update_files(request) -> dict[int, UploadedFile]:
    result = {}
    for key, file in request.FILES.items():
        match = UPDATE_FILE_KEY_RE.match(key)
        if match:
            image_id = int(match.group(1))
            result[image_id] = file
    return result
