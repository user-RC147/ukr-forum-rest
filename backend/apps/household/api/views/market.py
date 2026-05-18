from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.household.models import Market
from apps.household.api.serializers.market import MarketSerializer
from apps.household.permissions.group_permissions import IsGroupCreator,IsOwner


class MarketViewSet(ModelViewSet):

    """
    ViewSet для магазинів.

    list     — всі магазини (глобальні, бачать всі)
    retrieve — деталь магазину
    create   — будь-який залогінений може додати магазин
    update   — тільки той хто створив
    destroy  — тільки той хто створив
    """

    serializer_class = MarketSerializer

    def get_queryset(self):
        return Market.objects.all().select_related('created_by')
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)