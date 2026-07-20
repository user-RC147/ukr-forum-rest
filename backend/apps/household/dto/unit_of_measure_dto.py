from dataclasses import dataclass

@dataclass(frozen=True)
class UnitOfMeasureOutDTO:
    id: int
    name: str
    code: str

    

@dataclass(frozen=True)
class CreateUnitOfMeasureInDTO:
    name: str
    code: str

