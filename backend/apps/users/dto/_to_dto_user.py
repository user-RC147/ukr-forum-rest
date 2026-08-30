from core.dto.geo.location_dto import (
    Location_Id_InDTO,
    Location_Id_OutDTO,
    LocationOutDTO,
)
from .user_dto import (
    UserPublicOutDTO,
    UserPrivateUpdateInDTO,
    User_Id_PublicOutDTO,
    UserShortPublicOutDTO,
)

from apps.users.dto._to_dto_location import (
    _to_dto_out_location,
    _to_dto_out_public_location,
)


def _to_dto_short_public_user_out(data) -> UserShortPublicOutDTO:
    dto = UserShortPublicOutDTO(
        id=data.id,
        display_name=data.display_name,
    )
    return dto


def _to_dto_user_in(data) -> UserPrivateUpdateInDTO:
    return UserPrivateUpdateInDTO(
        display_name=data.get("display_name"),
        first_name=data.get("first_name"),
        first_name_public=data.get("first_name_public"),
        last_name=data.get("last_name"),
        last_name_public=data.get("last_name_public"),
        email=data.get("email"),
        email_public=data.get("email_public"),
        date_of_birth=data.get("date_of_birth"),
        date_of_birth_public=data.get("date_of_birth_public"),
        phone_number=data.get("phone_number"),
        phone_public=data.get("phone_public"),
        social_network=data.get("social_network"),
        social_public=data.get("social_public"),
        country_public=data.get("country_public"),
        region_public=data.get("region_public"),
        city_public=data.get("city_public"),
        location=Location_Id_InDTO(
            country_id=data["location"]["country_id"],
            region_id=data["location"]["region_id"],
            city_id=data["location"]["city_id"],
        ),
    )


def _to_dto_public_id_user_out(data) -> User_Id_PublicOutDTO:
    return User_Id_PublicOutDTO(
        id=data.id,
        display_name=data.display_name,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        date_of_birth=data.date_of_birth,
        phone_number=data.phone_number,
        social_network=data.social_network,
        location=Location_Id_OutDTO(
            country_id=data.country_id,
            region_id=data.region_id,
            city_id=data.city_id,
        ),
    )


def _to_dto_public_user_out(data, map_location) -> UserPublicOutDTO:

    dto = UserPublicOutDTO(
        id=data.id,
        display_name=data.display_name,
        first_name=data.first_name if data.first_name_public else None,
        last_name=data.last_name if data.last_name_public else None,
        email=data.email if data.email_public else None,
        date_of_birth=data.date_of_birth if data.date_of_birth_public else None,
        phone_number=data.phone_number if data.phone_public else None,
        social_network=data.social_network if data.social_public else None,
        location=(
            _to_dto_out_public_location(data, map_location) if data.location else None
        ),
    )

    return dto
