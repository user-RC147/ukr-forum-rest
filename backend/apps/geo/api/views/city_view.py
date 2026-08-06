from typing import Any

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.geo.api.schemas.city import city_search_schema
from apps.geo.api.serializers.resolve import (
    CitySearchQuerySerializer,
    CitySerializer,
)
from apps.geo.services.city_service import CityService


class CityView(viewsets.ViewSet):
    serializer_class = CitySerializer

    def __init__(self, service=CityService(), **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = service

    def retrieve(self, request: Request, id: int):
        result = self.service.get(id)

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    def list(self, request: Request):
        qp = CitySearchQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)

        result = self.service.get_by_region(qp.validated_data.get("region"))

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    @city_search_schema
    def search(self, request: Request):
        qp = CitySearchQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        query = qp.validated_data.get("q", "")
        if len(query) < 2:
            return Response({"results": [], "query": query})

        filtration = qp.validated_data.get("country_id")
        if filtration is None:
            filtration = qp.validated_data.get["region_id"]

        result = self.service.search(query, country_id=filtration)
        serializer = CitySerializer(result, many=True)
        return Response(serializer.data)
