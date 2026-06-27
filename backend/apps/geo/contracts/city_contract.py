from django.apps import apps

from apps.geo.services.geo_service import GeoService
from apps.geo.protocols.city import CityContractProtocol
from apps.geo.dto.city import CityDTO
from dataclasses import fields


class CityContract:
    def __init__(self, service: GeoService | None = None) -> None:
        # Зберігаємо переданий сервіс у приватну змінну
        self._service = service
        self._dto_fields = {f.name for f in fields(CityDTO)}

    @property
    def service(self) -> GeoService:
        """
        Ледаче отримання налаштованого сервісу з вашого оновленого GeoConfig.
        Тепер створення контракту повністю безпечне під час старту Django.
        """
        if self._service is None:
            self._service = apps.get_app_config('geo').service
        return self._service

    def get(self, city_id: int) -> CityDTO:
        # self.service автоматично звертається до property вище
        data = self.service.get_city(city_id)
        return self._to_dto(data)
    
    def get_many(self, city_ids: list[int]) -> dict[int, CityDTO]:
        # self.service автоматично звертається до property вище
        data = self.service.get_cities(city_ids)
        # return {d.id: self._to_dto(d) for d in data}
        return data

    def _to_dto(self, data) -> CityDTO:
        # Запобіжник на випадок, якщо місто не знайдено і повернувся None
        if data is None:
            return None
        return CityDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_city_contract() -> CityContractProtocol:
    return CityContract()