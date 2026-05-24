# # apps/geo/services/geo_service.py
# from typing import Optional
# from apps.geo.models import Country, Region, City
# from apps.geo.dto.geo_dto import CountryDTO, RegionDTO, CityDTO
# from apps.geo.clients.geo_api_client import geo_api_client
# from apps.geo.repositories.geo_repository import geo_repository


# class GeoService:

#     # -------------------------------------------------------
#     # Для фронту — реєстрація і зміна локації
#     # Беремо з зовнішнього API і зберігаємо в локальну БД
#     # -------------------------------------------------------

#     def fetch_and_save_countries(self) -> list[CountryDTO]:
#         """Отримує країни з зовнішнього API і зберігає в БД."""
#         api_countries = geo_api_client.get_countries()
#         result = []
#         for data in api_countries:
#             country = geo_repository.get_or_create_country(data)
#             result.append(CountryDTO(
#                 id=country.id,
#                 name=country.name,
#                 name_ua=country.name_ua,
#                 code=country.code,
#                 flag_emoji=country.flag_emoji,
#             ))
#         return result

#     def fetch_and_save_regions(self, country_code: str) -> list[RegionDTO]:
#         """Отримує регіони з зовнішнього API і зберігає в БД."""
#         # знаходимо країну в локальній БД
#         try:
#             country = Country.objects.get(code=country_code)
#         except Country.DoesNotExist:
#             return []

#         api_regions = geo_api_client.get_regions(country_code)
#         result = []
#         for data in api_regions:
#             region = geo_repository.get_or_create_region(data, country)
#             result.append(RegionDTO(
#                 id=region.id,
#                 name=region.name,
#                 name_ua=region.name_ua,
#             ))
#         return result

#     def fetch_and_save_cities(self, region_id: int) -> list[CityDTO]:
#         """Отримує міста з зовнішнього API і зберігає в БД."""
#         try:
#             region = Region.objects.select_related('country').get(id=region_id)
#         except Region.DoesNotExist:
#             return []

#         # шукаємо api_id регіону щоб запитати зовнішній API
#         if not region.api_id:
#             return []

#         api_cities = geo_api_client.get_cities(region.api_id)
#         result = []
#         for data in api_cities:
#             city = geo_repository.get_or_create_city(data, region.country, region)
#             result.append(CityDTO(
#                 id=city.id,
#                 name=city.name,
#                 name_ua=city.name_ua,
#             ))
#         return result

#     # -------------------------------------------------------
#     # Для внутрішніх модулів — тільки локальна БД
#     # -------------------------------------------------------

#     def get_country(self, country_id: int) -> Optional[CountryDTO]:
#         try:
#             c = Country.objects.get(id=country_id)
#             return CountryDTO(id=c.id, name=c.name, name_ua=c.name_ua,
#                               code=c.code, flag_emoji=c.flag_emoji)
#         except Country.DoesNotExist:
#             return None

#     def get_region(self, region_id: int) -> Optional[RegionDTO]:
#         try:
#             r = Region.objects.get(id=region_id)
#             return RegionDTO(id=r.id, name=r.name, name_ua=r.name_ua)
#         except Region.DoesNotExist:
#             return None

#     def get_city(self, city_id: int) -> Optional[CityDTO]:
#         try:
#             c = City.objects.get(id=city_id)
#             return CityDTO(id=c.id, name=c.name, name_ua=c.name_ua)
#         except City.DoesNotExist:
#             return None

#     def get_countries(self, ids: list[int]) -> list[CountryDTO]:
#         if not ids:
#             return []
#         return [
#             CountryDTO(id=c.id, name=c.name, name_ua=c.name_ua,
#                        code=c.code, flag_emoji=c.flag_emoji)
#             for c in Country.objects.filter(id__in=ids)
#         ]

#     def get_regions(self, ids: list[int]) -> list[RegionDTO]:
#         if not ids:
#             return []
#         return [
#             RegionDTO(id=r.id, name=r.name, name_ua=r.name_ua)
#             for r in Region.objects.filter(id__in=ids)
#         ]

#     def get_cities(self, ids: list[int]) -> list[CityDTO]:
#         if not ids:
#             return []
#         return [
#             CityDTO(id=c.id, name=c.name, name_ua=c.name_ua)
#             for c in City.objects.filter(id__in=ids)
#         ]


# geo_service = GeoService()


from typing import Optional
from core.contracts.geo import IGeoServiceContract
from core.dto.geo_dto import CountryDTO, RegionDTO, CityDTO
from apps.geo.repositories.geo_repository import GeoRepository
from apps.geo.clients.geo_api_client import geo_api_client  # Клієнт API поки залишаємо так, або теж прокинемо через init


class GeoService(IGeoServiceContract):
    """
    Реалізація гео-сервісу.
    Працює з репозиторієм для локальних даних та з клієнтом для зовнішнього API.
    """

    def __init__(self, repository: GeoRepository) -> None:
        # Впроваджуємо репозиторій через конструктор
        self._repository = repository

    # -------------------------------------------------------
    # Для фронту — реєстрація і зміна локації
    # -------------------------------------------------------

    def fetch_and_save_countries(self) -> list[CountryDTO]:
        """Отримує країни з зовнішнього API і зберігає в БД."""
        api_countries = geo_api_client.get_countries()
        result = []
        for data in api_countries:
            country = self._repository.get_or_create_country(data)
            result.append(CountryDTO(
                id=country.id,
                name=country.name,
                name_ua=country.name_ua,
                code=country.code,
            ))
        return result

    def fetch_and_save_regions(self, country_code: str) -> list[RegionDTO]:
        """Отримує регіони з зовнішнього API і зберігає в БД."""
        # ВИПРАВЛЕНО: Запит до БД перенесено в репозиторій
        country = self._repository.get_country_by_code(country_code)
        if not country:
            return []

        api_regions = geo_api_client.get_regions(country_code)
        result = []
        for data in api_regions:
            region = self._repository.get_or_create_region(data, country)
            result.append(RegionDTO(
                id=region.id,
                name=region.name,
                name_ua=region.name_ua,
                country_id=country.id
            ))
        return result

    def fetch_and_save_cities(self, region_id: int) -> list[CityDTO]:
        """Отримує міста з зовнішнього API і зберігає в БД."""
        # ВИПРАВЛЕНО: Запит до БД перенесено в репозиторій
        region = self._repository.get_region_by_id_with_country(region_id)
        if not region or not region.api_id:
            return []

        api_cities = geo_api_client.get_cities(region.api_id)
        result = []
        for data in api_cities:
            city = self._repository.get_or_create_city(data, region.country, region)
            result.append(CityDTO(
                id=city.id,
                name=city.name,
                name_ua=city.name_ua,
                region_id=region.id
            ))
        return result

    # -------------------------------------------------------
    # Реалізація IGeoServiceContract (Для внутрішніх модулів)
    # -------------------------------------------------------

    def is_country_exists(self, country_id: int) -> bool:
        """Перевіряє чи існує країна в локальній БД."""
        return self._repository.country_exists(country_id)

    def is_region_exists(self, region_id: int) -> bool:
        """Перевіряє чи існує регіон в локальній БД."""
        return self._repository.region_exists(region_id)

    def is_city_exists(self, city_id: int) -> bool:
        """Перевіряє чи існує місто в локальній БД."""
        return self._repository.city_exists(city_id)

    # -------------------------------------------------------
    # Додаткові методи для отримання DTO, якщо вони знадобляться іншим модулям
    # -------------------------------------------------------

    def get_city_by_id(self, city_id: int) -> Optional[CityDTO]:
        """Отримати інформацію про місто за його ID у вигляді DTO."""
        city = self._repository.get_city_by_id(city_id)
        if not city:
            return None
        return CityDTO(
            id=city.id,
            name=city.name,
            name_ua=city.name_ua,
            region_id=city.region_id
        )