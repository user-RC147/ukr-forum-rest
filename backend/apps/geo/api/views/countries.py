# apps/geo/api/views/countries.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.apps import apps
from dataclasses import asdict


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