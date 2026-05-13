from dataclasses import dataclass
from optparse import Option
from typing import Optional


@dataclass
class ProfileUpdateDTO:
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[str] = None
    social_network: Optional[str] = None
    consent_given: Optional[bool] = None