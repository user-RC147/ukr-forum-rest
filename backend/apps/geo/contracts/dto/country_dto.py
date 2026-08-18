from dataclasses import dataclass


@dataclass
class CountryDTO:
    id: int
    name: str
    name_ua: str
    code: str
    flag_emoji: str
    currency: str
