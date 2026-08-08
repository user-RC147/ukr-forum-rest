# apps/geo/api/views/cities.py
from dataclasses import asdict

from django.apps import apps
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.geo.api.schemas.city import city_search_schema
from apps.geo.api.serializers.resolve import CitySerializer


class CityListView(APIView):
    """
    GET /api/geo/cities/?region=5
    Бере з зовнішнього API і зберігає в локальну БД.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # 2. Отримуємо налаштований geo_service з IoC-контейнера
        geo_service = apps.get_app_config("geo").service

        region_id = request.query_params.get("region_id")
        if not region_id:
            return Response({"results1": []})
        cities = geo_service.fetch_and_save_cities(int(region_id))
        return Response({"results": [asdict(c) for c in cities]})


class CitySearchView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CitySerializer

    @city_search_schema
    def get(self, request: Request):
        query = request.query_params.get("q", "")
        country_id = request.query_params.get("country_id", "")
        if len(query) < 2 or not country_id:
            return Response({"results3": [], "query": query})

        geo_service = apps.get_app_config("geo").service
        serializer = CitySerializer(
            geo_service.search_cities(query, country_id), many=True
        )
        return Response(serializer.data)
