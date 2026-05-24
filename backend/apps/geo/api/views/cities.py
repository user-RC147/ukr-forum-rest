# apps/geo/api/views/cities.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.geo.services.geo_service import GeoService
from dataclasses import asdict


class CityListView(APIView):
    """
    GET /api/geo/cities/?region=5
    Бере з зовнішнього API і зберігає в локальну БД.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        region_id = request.query_params.get('region')
        if not region_id:
            return Response({'results': []})
        cities = geo_service.fetch_and_save_cities(int(region_id))
        return Response({'results': [asdict(c) for c in cities]})