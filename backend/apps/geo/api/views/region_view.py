from typing import Any

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.geo.api.serializers.resolve import (
    RegionQuerySerializer,
    RegionSerializer,
)
from apps.geo.services.region_service import get_service_region


class RegionView(viewsets.ViewSet):
    serializer_class = RegionSerializer

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = get_service_region()

    def retrieve(self, request: Request, pk: int):
        result = self.service.get(pk)

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    def list(self, request: Request):

        qp = RegionQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)

        result = self.service.get_by_country(qp.validated_data.get("country_id"))

        return Response(self.serializer_class(result, many=True).data, status=status.HTTP_200_OK)
