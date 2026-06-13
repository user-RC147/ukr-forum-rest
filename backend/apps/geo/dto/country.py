from dataclasses import dataclass

@dataclass
class CountryDTO:
    """
    Публічне представлення країни.
    Використовується іншими модулями — household, users тощо.
    """
    id: int
    name: str
    name_ua: str
    code: str
    flag_emoji: str