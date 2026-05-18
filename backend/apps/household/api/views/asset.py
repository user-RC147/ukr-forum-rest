from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.household.models import Asset
from apps.household.api.serializers.asset import AssetSerializer

from apps.household.permissions.group_permissions import IsGroupMember,IsGroupEditor,IsGroupCreator


class AssetViewSet(ModelViewSet):
    serializer_class=AssetSerializer
    
    def get_queryset(self):
        return Asset.objects.filter(
            group__members__user=self.request.user
        ).select_related('group')
    
    def get_permissions(self):
        if self.action in ['list','retrive']:
            return [IsAuthenticated(),IsGroupMember()]
        elif self.action in ['update','partial_update','create']:
            return [IsAuthenticated(),IsGroupEditor()]
        elif self.action == 'destroy':
            return [IsAuthenticated(),IsGroupCreator()]
        return [IsAuthenticated()]