from apps.household.dto.unit_of_measure_dto import CreateUnitOfMeasureInDTO
from apps.household.models.unit_of_measure import UnitOfMeasure


class UnitOfMeasureRepository:
    def create(self, dto: CreateUnitOfMeasureInDTO) -> UnitOfMeasure:
        """Створює нову одиницю виміру у базі даних."""
        unit = UnitOfMeasure.objects.create(
            name=dto.name,
        )
        return unit
