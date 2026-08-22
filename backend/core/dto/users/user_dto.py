from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.dto.geo.location_dto import Location_Id_OutDTO,LocationOutDTO


@dataclass(frozen=True)
class ConsentOutDTO:
    id:int
    version: str
    text: str
    created_at: datetime


@dataclass(frozen=True)
class UserShortOutDTO:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """

    id: int
    username: str
    display_name: str

class UserFullOutDTO:
    id: int
    username: str
    display_name: str

@dataclass(frozen=True)
class User_Id_PublicOutDTO:
    username: str
    display_name: str

    first_name:str
    first_name_public: bool

    last_name:str
    last_name_public: bool

    email:str
    email_public: bool

    date_of_birth: datetime
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    country_public:bool
    region_public:bool
    city_public:bool

@dataclass(frozen=True)
class User_Id_PrivateOutDTO:
    id:int
    username: str
    display_name: str

    first_name:str
    first_name_public: bool

    last_name:str
    last_name_public: bool

    email:str
    email_public: bool
    is_email_verified: bool

    date_of_birth: datetime
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    is_banned: bool

    deletion_scheduled_at: datetime

    consent_given: bool
    consent_date: datetime
    consent_version: Optional[ConsentOutDTO]

    country_public:bool
    region_public:bool
    city_public:bool

    location:Optional[Location_Id_OutDTO]


@dataclass(frozen=True)
class UserPublicOutDTO:
    id:int
    username: str
    display_name: str

    first_name_public: bool
    last_name_public: bool

    email:str
    email_public: str
    is_email_verified: bool

    date_of_birth: datetime
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    country_public:bool
    region_public:bool
    city_public:bool

    location:Optional[LocationOutDTO]
