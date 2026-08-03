# apps/users/dto/user_dto.py

# Реекспорт із core — єдина крапка входу для DTO юзера всередині цього модуля.
# Якщо users колись треба відв'язати від core — замінити цей імпорт власним class.

# далі — DTO, специфічні тільки для цього модуля:
# UserPrivateOutDTO, UserPublicOutDTO, User_Id_PrivateOutDTO тощо

import datetime
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

from core.dto.geo.location_dto import Location_Id_OutDTO, LocationOutDTO


