from django.apps import apps

from apps.geo.services.geo_service import GeoService
from apps.geo.protocols.region import RegionContractProtocol
from apps.geo.dto.region import RegionDTO
from dataclasses import fields


class RegionContract:
    def __init__(self, service: GeoService | None = None) -> None:
        # Зберігаємо переданий сервіс у приватну змінну (для тестів)
        self._service = service
        self._dto_fields = {f.name for f in fields(RegionDTO)}

    @property
    def service(self) -> GeoService:
        """
        Ледаче отримання налаштованого сервісу з вашого нового GeoConfig.
        Тепер це повністю безпечно і не викликає TypeError при старті.
        """
        if self._service is None:
            self._service = apps.get_app_config('geo').service
        return self._service

    def get_region(self, region_id: int, country_id: int) -> RegionDTO:
        # self.service тут автоматично викличе @property вище
        data = self.service.get_region(region_id, country_id)
        return self._to_dto(data)

    def _to_dto(self, data) -> RegionDTO:
        # Запобіжник: якщо регіон не знайдено в БД і повернувся None
        if data is None:
            return None
        return RegionDTO(**{field: getattr(data, field) for field in self._dto_fields})


def get_region_contract() -> RegionContractProtocol:
    return RegionContract()