from dataclasses import dataclass

@dataclass(frozen=True)
class UnitOfMeasureDTO:
    id: int
    name: str
    code: str

    

@dataclass(frozen=True)
class CreateUnitOfMeasureInDTO:
    name: str
    code: str

