# apps/geo/api/views/regions.py
from dataclasses import asdict

from django.apps import apps
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class RegionListView(APIView):
    """
    GET /api/geo/regions/?country_code=UA
    Бере з зовнішнього API і зберігає в локальну БД.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.data)

        # 2. Отримуємо налаштований geo_service з IoC-контейнера
        geo_service = apps.get_app_config("geo").service

        country_id = request.query_params.get("country_id", "")
        if not country_id:
            return Response({"results": []})
        regions = geo_service.fetch_and_save_regions(country_id)
        return Response({"results": [asdict(r) for r in regions]})
