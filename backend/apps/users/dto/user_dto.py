# apps/users/dto/user_dto.py

import datetime
from typing import Optional
from uuid import UUID
from datetime import date


from apps.geo.contracts.dto.country_dto import CountryDTO

from core.dto.users.user_dto import UserShortOutDTO
from core.dto.geo.geo_dto import (
    CountryShortDTO,
    RegionShortDTO,
    CityShortDTO,
    CityStarShortDTO,
)
from core.dto.geo.location_dto import (
    Location_Id_OutDTO,
    LocationOutDTO,
    Location_Id_InDTO,
)


from dataclasses import dataclass


@dataclass(frozen=True)
class ConsentOutDTO:
    id: int
    version: str
    text: str
    created_at: datetime


@dataclass(frozen=True)
class CreateUserInDTO:
    username: str
    password: str
    display_name: str
    email: str
    referral_code: UUID | None
    consent_given: bool


@dataclass(frozen=True)
class UserPrivateUpdateInDTO:
    display_name: str

    first_name: str
    first_name_public: bool

    last_name: str
    last_name_public: bool

    email: str
    email_public: bool

    date_of_birth: Optional[date]
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    country_public: bool
    region_public: bool
    city_public: bool

    location: Location_Id_InDTO

@dataclass(frozen=True)
class UserPrivateOutDTO:
    id: int
    username: str
    display_name: str

    first_name: str
    first_name_public: bool

    last_name: str
    last_name_public: bool

    email: str
    email_public: str

    date_of_birth: datetime
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    consent_given: bool
    consent_date: datetime
    consent_version: Optional[ConsentOutDTO]

    country_public: bool
    region_public: bool
    city_public: bool

    location: Optional[LocationOutDTO]


@dataclass(frozen=True)
class User_Id_PublicOutDTO:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """
    id:int
    display_name: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    phone_number: str
    social_network: str
    location:Location_Id_OutDTO


@dataclass(frozen=True)
class User_Id_PrivateOutDTO:
    id: int
    username: str
    display_name: str

    first_name: str
    first_name_public: bool

    last_name: str
    last_name_public: bool

    email: str
    email_public: bool

    date_of_birth: datetime
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool


    consent_given: bool
    consent_date: datetime
    consent_version: ConsentOutDTO | None

    country_public: bool
    region_public: bool
    city_public: bool

    location: Optional[Location_Id_OutDTO]


@dataclass(frozen=True)
class UserPublicOutDTO:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """

    id: int
    display_name: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    phone_number: str
    social_network: str
    location: LocationOutDTO | None


@dataclass(frozen=True)
class UserShortPublicOutDTO:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """
    id: int
    display_name: str

