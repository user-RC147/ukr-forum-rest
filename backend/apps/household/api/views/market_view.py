from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema

from core.users.csrf_permission import CsrfPermission

from apps.household.api.serializers.market_serializer import (
    MarketSerializer,
    MarketCreateSerializer,
    MarketFullSerializer,
)
from apps.household.dto.location_dto import Location_Id_InDTO
from apps.household.permissions.group_permissions import IsGroupCreator, IsOwner
from apps.household.dto.market_dto import (
    CreateMarketInDTO,
    ListMarketDTO,
    MarketFullOutDTO,
)
from apps.household.services.market_service import MarketService


class MarketViewSet(ViewSet):
    """
    ViewSet для магазинів.

    list     — всі магазини (глобальні, бачать всі)
    retrieve — деталь магазину
    create   — будь-який залогінений може додати магазин
    update   — тільки той хто створив
    destroy  — тільки той хто створив
    """

    def get_permissions(self):
        if self.action in []: #"list", "retrieve"
            return [AllowAny(), CsrfPermission()]
        return [IsAuthenticated(), CsrfPermission()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._service = MarketService()

    def list(self, request):
        """
        GET /api/household/markets/
        """

        markets_data = self._service.get_all()
        serializer = MarketFullSerializer(markets_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=MarketCreateSerializer, responses=MarketSerializer)
    def create(self, request):
        """
        POST /api/household/markets/
        Створення нового магазину. Викликається кнопкою з форми чека.
        """

        serializer = MarketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        dto = CreateMarketInDTO(
            name=vd["name"],
            address_line=vd["address_line"],
            location=Location_Id_InDTO(
                country_id=vd["country_id"],
                region_id=vd["region_id"],
                city_id=vd["city_id"],
            ),
        )

        market = self._service.create(dto=dto, user=request.user.id)
        return Response(MarketSerializer(market).data, status=status.HTTP_201_CREATED)

    # def retrieve(self, request, pk=None):
    #     pass

    # def update(self, request, pk=None):
    #     pass

    # def partial_update(self, request, pk=None):
    #     pass

    # def destroy(self, request, pk=None):
    #     pass
