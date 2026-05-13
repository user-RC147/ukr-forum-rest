from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterDTO:
    username: str
    email: str
    pessword: str
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None