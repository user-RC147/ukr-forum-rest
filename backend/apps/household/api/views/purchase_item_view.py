from unittest import result
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ViewSet


from apps.household.api.serializers.purchase_serializer import PurchaseItemOutSerializer
from apps.household.services.purchase_item_service import PurchaseItemService


class PurchaseItemViewSet(ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._service = PurchaseItemService()



    def list(self, request):
        user_id = request.user.id

        purchase_items = self._service.get_all_purchase_item(user_id)

        serializer = PurchaseItemOutSerializer(purchase_items,many=True)

        results = serializer.data

        return Response({'results':results}, status=status.HTTP_200_OK)

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
