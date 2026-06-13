from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.household.models import Purchase
from apps.household.api.serializers.purchase import PurchaseSerializer
from apps.household.permissions.group_permissions import (
    IsGroupMember,
    IsGroupEditor,
    IsGroupCreator,
)


class PurchaseViewSet(ModelViewSet):
    """
    ViewSet для чеків.

    list     — всі чеки груп де користувач є учасником
    retrieve — деталь чеку з усіма рядками
    create   — створити чек з рядками одним запитом
    update   — оновити чек і рядки (editor, creator)
    destroy  — видалити чек (creator)
    """

    serializer_class = PurchaseSerializer

    def get_queryset(self):
        return (
            Purchase.objects.filter(asset__group__members__user=self.request.user)
            .select_related(
                "asset",
                "market",
                "created_by",
            )
            .prefetch_related("items__product")
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated(), IsGroupMember()]
        elif self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated(), IsGroupEditor()]
        elif self.action == "destroy":
            return [IsAuthenticated(), IsGroupCreator()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
