from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

# Імпортуємо серіалізатор чеків
from apps.household.api.serializers import CreatePurchaseSerializer

from apps.household.api.serializers.purchase_serializer import PurchaseOutSerializer,Purchase_Id_OutSerializer
from apps.household.dto.purchase_dto import Purchase_Id_OutDTO
from apps.household.services.purchase_service import PurchaseService
from apps.household.dto import CreatePurchaseInDTO, PurchaseItemInDTO

# функція-тимчасова для перевірки реквеста
from core.func_request import func_request


class PurchaseViewSet(viewsets.ViewSet):
    """
    ViewSet для управління чеками (Purchases) через шари сервісів.
    Контролер для управління чеками та витратами.
    Працює виключно з авторизованими користувачами платформи.
    """

    # Захищаємо ендпоінт: тільки зареєстровані юзери мають доступ до модуля household
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = PurchaseService()

    def list(self, request):
        user_id = request.user.id

        purchase_list = self._service.get_all_purchase(user_id)

        serializer = PurchaseOutSerializer(purchase_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=CreatePurchaseSerializer, responses=PurchaseOutSerializer)
    def create(self, request):

        creator_user_id = request.user.id

        serializer = CreatePurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        dto = CreatePurchaseInDTO(
            asset_id=data["asset_id"],
            market_id=data["market_id"],
            data_purchase=data["data_purchase"],
            items=[
                PurchaseItemInDTO(
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    price_per_unit=item["price_per_unit"],
                )
                for item in data["items"]
            ],
        )
        create_purchase = self._service.create(
            dto=dto, creator_user_id=creator_user_id
        )

        serializer = Purchase_Id_OutSerializer(create_purchase)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
