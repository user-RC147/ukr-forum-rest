from typing import Any

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.geo.api.schemas import city_search_schema, country_search_schema
from apps.geo.api.serializers import (
    CityQuerySerializer,
    CitySearchQuerySerializer,
    CitySerializer,
    CountrySerializer,
    RegionQuerySerializer,
    RegionSerializer,
    SearchQuerySerializer,
)
from apps.geo.services.city_service import get_service_city
from apps.geo.services.country_service import get_service_country
from apps.geo.services.region_service import get_service_region


class CityView(viewsets.ViewSet):
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = get_service_city()

    def retrieve(self, request: Request, pk: int):
        result = self.service.get(pk)

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    def list(self, request: Request):
        qp = CityQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)

        result = self.service.get_by_region(qp.validated_data.get("region_id"))

        return Response(
            self.serializer_class(result, many=True).data, status=status.HTTP_200_OK
        )

    @city_search_schema
    @action(methods=["get"], detail=False)
    def search(self, request: Request):
        qp = CitySearchQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        query = qp.validated_data.get("q", "")
        if len(query) < 2:
            return Response({"results": [], "query": query})

        filtration = qp.validated_data.get("country_id")

        result = self.service.search(query, country_id=filtration)
        serializer = CitySerializer(result, many=True)
        return Response(serializer.data)


class CountryView(viewsets.ViewSet):
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.service = get_service_country()

    def retrieve(self, request: Request, pk: int):
        result = self.service.get(pk)

        return Response(self.serializer_class(result).data, status=status.HTTP_200_OK)

    def list(self, request: Request):
        result = self.service.get_many()

        return Response(
            self.serializer_class(result, many=True).data, status=status.HTTP_200_OK
        )

    @country_search_schema
    @action(methods=["get"], detail=False)
    def search(self, request: Request):
        qp = SearchQuerySerializer(data=request.query_params)
        qp.is_valid(raise_exception=True)
        query = qp.validated_data.get("q", "")
        if len(query) < 2:
            return Response({"results": [], "query": query})

        result = self.service.search(query)
        serializer = CountrySerializer(result, many=True)
        return Response(serializer.data)


class RegionView(viewsets.ViewSet):
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]

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

        return Response(
            self.serializer_class(result, many=True).data, status=status.HTTP_200_OK
        )
