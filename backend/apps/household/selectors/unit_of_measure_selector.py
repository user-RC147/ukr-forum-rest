from apps.household.models.unit_of_measure import UnitOfMeasure
from apps.household.exceptions.unit_of_measure_exception import UnitOfMeasureNotFoundException 



class UnitOfMeasureSelector:

    def get_all_units(self):
        return UnitOfMeasure.objects.all().order_by('id')
        
    def get_name_by_id(self, unit_of_measure_id: int):
        try:
            return UnitOfMeasure.objects.get(id=unit_of_measure_id).name
        except UnitOfMeasure.DoesNotExist:
            raise UnitOfMeasureNotFoundException(unit_of_measure_id=unit_of_measure_id)
