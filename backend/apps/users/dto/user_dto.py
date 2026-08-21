# apps/users/dto/user_dto.py

import datetime
from typing import Optional
from uuid import UUID



from core.dto.users.user_dto import ConsentOutDTO,UserShortOutDTO,User_Id_PrivateOutDTO
from core.dto.geo.geo_dto import CountryShortDTO,RegionShortDTO, CityShortDTO
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
    display_name: Optional[str] = None

    first_name_public: Optional[bool] = None
    last_name_public: Optional[bool] = None

    email:Optional[str] = None
    email_public: Optional[str] = None

    date_of_birth: Optional[datetime] = None
    date_of_birth_public: Optional[bool] = None

    phone_number: Optional[str] = None
    phone_public: Optional[bool] = None

    social_network: Optional[str] = None
    social_public: Optional[bool] = None
    
    location:Optional[Location_Id_InDTO] = None



@dataclass(frozen=True)
class UserPrivateOutDTO:
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

    is_banned: bool

    deletion_scheduled_at: datetime

    consent_given: bool
    consent_date: datetime
    consent_version: Optional[ConsentOutDTO]
    location:Optional[LocationOutDTO]

