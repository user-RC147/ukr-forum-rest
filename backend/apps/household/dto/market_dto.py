from dataclasses import dataclass

@dataclass(frozen=True)
class ListMarketDTO:
    name:int
    


@dataclass(frozen=True)
class CreateMarketInDTO:
    name:str
    address_line: str
    country_id:int
    region_id:int
    city_id:int


@dataclass(frozen=True)
class MarketOutDTO:
    id:int
    name:str
    address_line: str
    country_id:int
    region_id:int
    city_id:int