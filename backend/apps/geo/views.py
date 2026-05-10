# apps/geo/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status

from apps.geo.services import geo_service


class CountryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            data = geo_service.get_countries()
        except RuntimeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data)


class RegionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        country_code = request.query_params.get("country_code")
        try:
            data = geo_service.get_regions(country_code=country_code)
        except RuntimeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data)


class CityListView(APIView):
    permission_classes = [AllowAny] #IsAuthenticated

    def get(self, request):
        region_id = request.query_params.get("region")
        search    = request.query_params.get("search")
        try:
            data = geo_service.get_cities(region_id=region_id, search=search)
        except RuntimeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data)