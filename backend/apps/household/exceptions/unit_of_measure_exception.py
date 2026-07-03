
class UnitOfMeasureNotFoundException(Exception):
    def __init__(self, unit_of_measure_id: int):
        self.unit_of_measure_id = unit_of_measure_id
        super().__init__(f"Unit of measure with ID {unit_of_measure_id} not found.")