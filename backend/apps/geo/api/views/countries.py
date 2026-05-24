# apps/geo/api/views/countries.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.geo.services.geo_service import GeoService
from dataclasses import asdict


class CountryListView(APIView):
    """
    GET /api/geo/countries/
    Бере з зовнішнього API і зберігає в локальну БД.
    Використовується тільки при реєстрації і зміні локації.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        countries = geo_service.fetch_and_save_countries()
        return Response([asdict(c) for c in countries])