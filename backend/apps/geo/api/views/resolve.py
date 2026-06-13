from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.geo.services.geo_service import geo_service
from apps.geo.api.serializers.resolve import CountrySerializer,RegionSerializer,CitySerializer


class GeoResolveView(APIView):
    
    """
    GET /api/geo/resolve/

    Резолвить ids країн, регіонів і міст в повні об'єкти.
    Використовується фронтом після отримання даних з інших модулів.

    Параметри запиту:
        country_ids=1,2,3
        region_ids=4,5
        city_ids=6,7,8

    Приклад:
        GET /api/geo/resolve/?country_ids=1&city_ids=5,12

    Відповідь:
        {
            "countries": [{"id": 1, "name": "Україна", ...}],
            "regions": [],
            "cities": [{"id": 5, ...}, {"id": 12, ...}]
        }
    """

    permission_classes=[IsAuthenticated]


    def _parse_ids(self,param:str)->list[int]:
        """
        Парсить рядок ids з query params.
        '1,2,3' → [1, 2, 3]
        Ігнорує невалідні значення.
        """
        if not param:
            return []
        result=[]

        for raw in param.split(','):
            try:
                result.append(int(raw.strip()))
            except ValueError:
                continue
        return result
    

    def get(self,request):
        country_ids=self._parse_ids(request.query_params.get('country_ids',''))
        region_ids=self._parse_ids(request.query_params.get('region_ids',''))
        city_ids=self._parse_ids(request.query_params.get('city_ids',''))

        # резолвимо через geo_service — не імпортуємо моделі напряму
        countries=[
            geo_service.get_country(id)
            for id in country_ids
        ]
        regions=[
            geo_service.get_region(id)
            for id in region_ids
        ]
        cities=[
            geo_service.get_city(id)
            for id in city_ids
        ]

        # фільтруємо None — якщо id не знайдено
        countries = geo_service.get_countries(country_ids)
        regions   = geo_service.get_regions(region_ids)
        cities    = geo_service.get_cities(city_ids)

        return Response({
            'countries':CountrySerializer(countries,many=True).data,
            'regions':RegionSerializer(regions,many=True).data,
            'cities':CitySerializer(cities,many=True).data,
        })
