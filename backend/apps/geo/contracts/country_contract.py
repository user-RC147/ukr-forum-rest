from dataclasses import fields

from django.apps import apps

from apps.geo.dto.country import CountryDTO
from apps.geo.protocols.country import CountryContractProtocol
from apps.geo.services.geo_service import GeoService


class CountryContract:
    def __init__(self, service: GeoService | None = None) -> None:
        # Зберігаємо сервіс, якщо його передали явно (наприклад, у тестах)
        self._service = service
        self._dto_fields = {f.name for f in fields(CountryDTO)}

    @property
    def service(self) -> GeoService:
        """Ледаче отримання налаштованого сервісу з IoC-контейнера Django"""
        if self._service is None:
            self._service = apps.get_app_config("geo").service
        return self._service

    def get(self, country_id: int) -> CountryDTO:
        # Тепер self.service викликає property вище і повертає повністю готовий сервіс
        data = self.service.get_country(country_id)
        return self._to_dto(data)

    def get_many(self, countries_ids: list[int]) -> dict[int, CountryDTO]:
        data = self.service.get_countries(countries_ids)
        return {d.id: self._to_dto(d) for d in data}

    def _to_dto(self, data) -> CountryDTO:
        # Якщо даних немає (None), повертаємо None або обробляємо помилку
        if data is None:
            return None
        return CountryDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_country_contract() -> CountryContractProtocol:
    return CountryContract()
