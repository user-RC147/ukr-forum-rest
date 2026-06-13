# apps/geo/api/views/regions.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.geo.services.geo_service import geo_service
from dataclasses import asdict


class RegionListView(APIView):
    """
    GET /api/geo/regions/?country_code=UA
    Бере з зовнішнього API і зберігає в локальну БД.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        country_code = request.query_params.get('country_code', '')
        if not country_code:
            return Response({'results': []})
        regions = geo_service.fetch_and_save_regions(country_code)
        return Response({'results': [asdict(r) for r in regions]})