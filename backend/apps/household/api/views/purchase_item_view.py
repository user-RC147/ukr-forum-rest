from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from core.users.csrf_permission import CsrfPermission

from apps.household.api.serializers.paginator_purchase_item_serializer import (
    PaginatorSerializerOut,
)
from apps.household.api.serializers.purchase_serializer import PurchaseItemOutSerializer
from apps.household.services.purchase_item_service import PurchaseItemService


class PurchaseItemViewSet(ViewSet):

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny(), CsrfPermission()]
        return [IsAuthenticated(), CsrfPermission()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = PurchaseItemService()

    def list(self, request):
        user_id = request.user.id
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 5))
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")

        purchase_items = self._service.get_all_purchase_item(
            user_id, page, page_size, date_from, date_to
        )

        results = PurchaseItemOutSerializer(purchase_items.items, many=True).data
        paginator = PaginatorSerializerOut(purchase_items)

        return Response(
            {"results": results, "paginator": paginator.data}, status=status.HTTP_200_OK
        )

    # def create(self, request):
    #     pass

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
