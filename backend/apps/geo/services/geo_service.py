# apps/geo/services/geo_service.py

import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.manager import BaseManager
from requests import RequestException

from apps.geo.clients.geo_api_client import geo_api_client
from apps.geo.dto.city import CityDTO
from apps.geo.dto.country import CountryDTO
from apps.geo.dto.region import RegionDTO
from apps.geo.models import City, Country, Region
from apps.geo.repositories.geo_repository import geo_repository
from dataclasses import asdict
logger = logging.getLogger(__name__)


class GeoService:
    def __init__(self, repository):
        self.repository = repository

    # -------------------------------------------------------
    # Для фронту — реєстрація і зміна локації
    # Беремо з зовнішнього API і зберігаємо в локальну БД
    # -------------------------------------------------------

    def fetch_and_save_countries(self) -> list[CountryDTO]:
        """Отримує країни з зовнішнього API і зберігає в БД. Якщо API лежить — бере з локальної БД."""
        try:
            # Пробуємо отримати дані з зовнішнього API
            api_countries = geo_api_client.get_countries()
            result = []
            for data in api_countries:
                country = geo_repository.get_or_create_country(data)
                result.append(
                    CountryDTO(
                        id=country.id,
                        name=country.name,
                        name_ua=country.name_ua,
                        code=country.code,
                        flag_emoji=country.flag_emoji,
                    )
                )
            return result
        except (RequestException, Exception) as e:
            # Якщо api.ukrkolo.site недоступний або впав по таймауту:
            print(f"Зовнішній гео-API недоступний ({e}). Беремо країни з локальної БД.")

            # Повертаємо всі країни, які вже встигли зберегтися в локальній БД раніше
            return [_to_dto_country(c) for c in Country.objects.all()]

    def fetch_and_save_regions(self, country_id: int) -> list[RegionDTO]:
        """Отримує регіони з зовнішнього API і зберігає в БД. Якщо API лежить — бере з локальної БД."""
        # Знаходимо країну в локальній БД
        try:
            country = Country.objects.get(id=country_id)
        except Country.DoesNotExist:
            return []

        try:
            # Пробуємо отримати регіони з зовнішнього API
            api_regions = geo_api_client.get_regions(country_id)
            result = []
            for data in api_regions:
                region = geo_repository.get_or_create_region(data, country)
                result.append(
                    RegionDTO(
                        id=region.id,
                        name=region.name,
                        name_ua=region.name_ua,
                        country_id=region.country_id,  # Задовольняємо вимогу RegionDTO
                    )
                )
            return result
        except (RequestException, Exception) as e:
            # Якщо зовнішній сервіс недоступний:
            print(
                f"Зовнішній гео-API недоступний ({e}). Беремо регіони з локальної БД."
            )

            # Повертаємо регіони цієї країни, які вже є в локальній базі
            return [_to_dto_region (r) for r in Region.objects.filter(country=country)]

    def fetch_and_save_cities(self, region_id: int) -> list[CityDTO]:
        """Отримує міста з зовнішнього API і зберігає в БД. Якщо API лежить — бере з локальної БД."""
        try:
            region = Region.objects.select_related("country").get(id=region_id)
        except Region.DoesNotExist:
            return []

        # Створюємо DTO регіону заздалегідь для передачі в CityDTO
        region_dto = self.get_region(region_id)

        if not region.api_id:
            # Якщо немає api_id, віддаємо локальні міста
            return [
                CityDTO(
                    id=c.id,
                    name=c.name,
                    name_ua=c.name_ua,
                    country_id=c.country_id,
                    region=asdict(region_dto), # Змінено з region_id на region
                )
                for c in City.objects.filter(region_id=region_id)
            ]

        try:
            # Пробуємо отримати міста із зовнішнього сайту
            api_cities = geo_api_client.get_cities(region.api_id)
            result = []
            for data in api_cities:
                city = geo_repository.get_or_create_city(data, region.country, region)
                result.append(
                    CityDTO(
                        id=city.id,
                        name=city.name,
                        name_ua=city.name_ua,
                        country_id=city.country_id,
                        region=asdict(region_dto), # Змінено з region_id на region
                    )
                )
            return result
        except (RequestException, Exception) as e:
            print(f"Зовнішній гео-API недоступний ({e}). Беремо міста з локальної БД.")

            # Повертаємо міста цього регіону з локальної БД
            return [
                CityDTO(
                    id=c.id,
                    name=c.name,
                    name_ua=c.name_ua,
                    country_id=c.country_id,
                    region=asdict(region_dto), # Змінено з region_id на region
                )
                for c in City.objects.filter(region_id=region_id)
            ]

    # -------------------------------------------------------
    # Для внутрішніх модулів — тільки локальна БД
    # -------------------------------------------------------

    def get_country(self, country_id: int) -> CountryDTO | None:
        try:
            c = Country.objects.get(id=country_id)
            return _to_dto_country(c)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    def get_region(self, region_id: int) -> RegionDTO | None:
        try:
            r = Region.objects.get(id=region_id)
            return _to_dto_region(r)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    def get_city(self, city_id: int) -> CityDTO | None:
        try:
            c = City.objects.get(id=city_id)
            return _to_dto_city(c, self.get_region(c.region_id))
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist

    def get_countries(self, ids: list[int]) -> list[BaseManager[Country]]:
        if not ids:
            return []

        countries = self.repository.get_countries(ids)

        found_ids = [c.id for c in countries]
        missing = set(ids) - set(found_ids)
        if missing:
            logger.warning("Countries not found for ids: %s", missing)

        return countries

    def get_regions(self, ids: list[int]) -> list[BaseManager[Region]]:
        if not ids:
            return []

        regions = self.repository.get_regions(ids)

        found_ids = [r.id for r in regions]
        missing = set(ids) - set(found_ids)
        if missing:
            logger.warning("Regions not found for ids: %s", missing)

        return regions

    def get_cities(self, ids: list[int]) -> dict[int, CityDTO]:
        if not ids:
            return []

        cities = self.repository.get_cities(ids)

        found_ids = [c.id for c in cities]
        missing = set(ids) - set(found_ids)
        if missing:
            logger.warning("Cities not found for ids: %s", missing)

        return {c.id: _to_dto_city(c, self.get_region(c.region_id)) for c in cities}
    
    def search_countries(self, query: str, limit: int = 10) -> list[CountryDTO]:
        query = query.strip()
        if len(query) < 2:
            return []
        objs = self.repository.search_country(query, limit)
        return [_to_dto_country(obj) for obj in objs]
    
    def search_cities(self, query: str, country_id: int, limit: int = 10) -> list[CityDTO]:
        query = query.strip()
        if len(query) < 2:
            return []
        objs = self.repository.search_city(query, country_id, limit)
        return [_to_dto_city(obj, self.get_region(obj.region.id)) for obj in objs]


    def is_country_exists(self, country_id: int) -> bool:
        return Country.objects.filter(id=country_id).exists()

    def is_region_exists(self, region_id: int) -> bool:
        return Region.objects.filter(id=region_id).exists()

    def is_city_exists(self, city_id: int) -> bool:
        return City.objects.filter(id=city_id).exists()

def _to_dto_country(data: Country) -> CountryDTO:
                return CountryDTO(
                id=data.id,
                name=data.name,
                name_ua=data.name_ua,
                code=data.code,
                flag_emoji=data.flag_emoji,
                currency=data.currency,
            )

def _to_dto_region(data: Region) -> RegionDTO:
                return RegionDTO(
                id=data.id,
                name=data.name,
                name_ua=data.name_ua,
                country_id=data.country.id
            )

def _to_dto_city(data: City, region: RegionDTO) -> CityDTO:
                return CityDTO(
                id=data.id,
                name=data.name,
                name_ua=data.name_ua,
                country_id=data.country.id,
                region=asdict(region),
                latitude=data.latitude,
                longitude=data.longitude
            )