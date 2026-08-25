# apps/users/dto/user_dto.py

import datetime
from typing import Optional
from uuid import UUID
from datetime import date


from apps.geo.contracts.dto.country_dto import CountryDTO

from core.dto.users.user_dto import ConsentOutDTO,UserShortOutDTO,User_Id_PrivateOutDTO
from core.dto.geo.geo_dto import CountryShortDTO,RegionShortDTO, CityShortDTO,CityStarShortDTO
from core.dto.geo.location_dto import Location_Id_OutDTO, LocationOutDTO,Location_Id_InDTO



from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserInDTO:
    username: str
    password:str
    display_name: str
    email:str
    referral_code: UUID | None
    consent_given:bool



@dataclass(frozen=True)
class ProfilUserUpdateInDTO:
    display_name: str

    first_name:str
    first_name_public: bool

    last_name:str
    last_name_public: bool

    email:str
    email_public: bool

    date_of_birth:  Optional[date]
    date_of_birth_public: bool

    phone_number: str
    phone_public: bool

    social_network: str
    social_public: bool

    country_public:bool
    region_public:bool
    city_public:bool
    
    location:Location_Id_InDTO



@dataclass(frozen=True)
class UserPrivateOutDTO:
    id:int
    username: str
    display_name: str

    first_name:str
    first_name_public: bool

    last_name:str
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

    is_banned: bool

    deletion_scheduled_at: datetime

    consent_given: bool
    consent_date: datetime
    consent_version: Optional[ConsentOutDTO]

    country_public:bool
    region_public:bool
    city_public:bool

    location:Optional[LocationOutDTO]


@dataclass(frozen=True)
class UserStarIdOutDTO:
    id:int
    location:Optional[Location_Id_OutDTO]

@dataclass(frozen=True)
class UserStarOutDTO:
    id:int
    location:Optional[LocationOutDTO]


@dataclass(frozen=True)
class StarShoyOutDTO:
    country:CountryDTO
    cities:list[CityStarShortDTO]
