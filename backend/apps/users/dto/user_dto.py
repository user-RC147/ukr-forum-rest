# apps/users/dto/user_dto.py

# Реекспорт із core — єдина крапка входу для DTO юзера всередині цього модуля.
# Якщо users колись треба відв'язати від core — замінити цей імпорт власним class.

# далі — DTO, специфічні тільки для цього модуля:
# UserPrivateOutDTO, UserPublicOutDTO, User_Id_PrivateOutDTO тощо

import datetime
from typing import Optional
from uuid import UUID
from core.dto.users.user_dto import (
    UserShortOutDTO,
    UserFullOutDTO,
    UserPublicOutDTO,
    UserPrivateOutDTO,
    User_Id_PublicOutDTO,
    User_Id_PrivateOutDTO,
    ConsentOutDTO,
)

from core.dto.geo.geo_dto import (
    CountryShortDTO,
    CountryOutDTO,
    RegionShortDTO,
    RegionOutDTO,
    CityShortDTO,
    CityOutDTO,
    
)

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
class UserDTO:
    ...

@dataclass(frozen=True)
class ProfilUserUpdateInDTO:
    username: Optional[str] = None
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