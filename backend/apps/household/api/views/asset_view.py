from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from yaml import serialize

from apps.household.apps import HouseholdConfig
from apps.household.api.serializers.asset_serializer import AssetSerializer


class AssetViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service=HouseholdConfig.asset_service



    def list(self, request):
        """Повертає активи для селекту на сторінці створення чека."""
        assets=self.service.get_user_assets(user_id=request.user.id)
        serializer=AssetSerializer(assets,many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass