# apps/geo/api/views/resolve.py
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.geo.api.serializers.resolve import CountrySerializer, RegionSerializer, CitySerializer


class GeoResolveView(APIView):
    """
    GET /api/geo/resolve/

    Резолвить ids країн, регіонів і міст в повні об'єкти.
    Використовується фронтом після отримання даних з інших модулів.
    """
    permission_classes = [IsAuthenticated]

    def _parse_ids(self, param: str) -> list[int]:
        """
        Парсить рядок ids з query params.
        '1,2,3' → [1, 2, 3]
        Ігнорує невалідні значення.
        """
        if not param:
            return []
        result = []

        for raw in param.split(','):
            try:
                result.append(int(raw.strip()))
            except ValueError:
                continue
        return result

    def get(self, request):
        # 1. Парсимо ID з query-параметрів
        country_ids = self._parse_ids(request.query_params.get('country_ids', ''))
        region_ids = self._parse_ids(request.query_params.get('region_ids', ''))
        city_ids = self._parse_ids(request.query_params.get('city_ids', ''))

        # 2. Отримуємо налаштований geo_service з IoC-контейнера
        geo_service = apps.get_app_config('geo').service

        # 3. Викликаємо ефективні масові методи сервісу (БЕЗ циклів та дублювання)
        countries = geo_service.get_countries(country_ids) if country_ids else []
        regions = geo_service.get_regions(region_ids) if region_ids else []
        cities = geo_service.get_cities(city_ids) if city_ids else []

        # 4. Повертаємо серіалізовану відповідь
        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'regions': RegionSerializer(regions, many=True).data,
            'cities': CitySerializer(cities, many=True).data,
        })