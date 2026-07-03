# apps/geo/api/views/countries.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.geo.api.schemas.country import country_search_schema
from django.apps import apps
from dataclasses import asdict
from rest_framework.request import Request
from apps.geo.api.serializers.resolve import CountrySerializer

class CountryListView(APIView):
    """
    GET /api/geo/countries/
    Бере з зовнішнього API і зберігає в локальну БД.
    Використовується тільки при реєстрації і зміні локації.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 2. Отримуємо налаштований geo_service з IoC-контейнера
        geo_service = apps.get_app_config('geo').service
        
        countries = geo_service.fetch_and_save_countries()
        return Response([asdict(c) for c in countries])

class CountrySearchView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CountrySerializer

    @country_search_schema
    def get(self, request: Request):
        query = request.query_params.get("q", "")
        if len(query) < 2:
            return Response({"results": [], "query": query})

        geo_service = apps.get_app_config('geo').service
        serializer = CountrySerializer(geo_service.search_countries(query), many=True)
        return Response(serializer.data)