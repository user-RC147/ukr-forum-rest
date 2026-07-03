from apps.household.selectors.unit_of_measure_selector import UnitOfMeasureSelector
from apps.household.repositories.unit_of_measure_repo import UnitOfMeasureRepository
from apps.household.dto.unit_of_measure_dto import CreateUnitOfMeasureInDTO


class UnitOfMeasureService:

    def __init__(self)->None:
        self._repository = UnitOfMeasureRepository()
        self._selector =UnitOfMeasureSelector()
    

    def get_all_units(self):
        return self._selector.get_all_units()


    def create(self, dto: CreateUnitOfMeasureInDTO):
        return self._repository.create(dto)