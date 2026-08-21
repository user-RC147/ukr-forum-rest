from apps.users.dto.user_dto import User_Id_PrivateOutDTO, ConsentOutDTO

from apps.users.dto._to_dto_location import (
    _to_dto_out_id_location,
    _to_dto_out_location,
)
from apps.users.dto.user_dto import UserPrivateOutDTO


def _to_dto_out_consent(data) -> ConsentOutDTO:
    return ConsentOutDTO(
        id=data.id,
        version=data.version,
        text=data.text,
        created_at=data.created_at,
    )


def _to_dto_id_location_profile(data) -> User_Id_PrivateOutDTO:
    return User_Id_PrivateOutDTO(
        id=data.id,
        username=data.username,
        display_name=data.display_name,
        first_name_public=data.first_name_public,
        last_name_public=data.last_name_public,
        email=data.email,
        email_public=data.email_public,
        is_email_verified=data.is_email_verified,
        date_of_birth=data.date_of_birth,
        date_of_birth_public=data.date_of_birth_public,
        phone_number=data.phone_number,
        phone_public=data.phone_public,
        social_network=data.social_network,
        social_public=data.social_public,
        is_banned=data.is_banned,
        deletion_scheduled_at=data.deletion_scheduled_at,
        consent_given=data.consent_given,
        consent_date=data.consent_date,
        consent_version=(
            _to_dto_out_consent(data.consent_version) if data.consent_version else None
        ),
        location=(
            _to_dto_out_id_location(data) if data.country_id else None
        ),
    )


def _to_dto_out_profile(data, map_location) -> UserPrivateOutDTO:
    return UserPrivateOutDTO(
        id=data.id,
        username=data.username,
        display_name=data.display_name,
        first_name_public=data.first_name_public,
        last_name_public=data.last_name_public,
        email=data.email,
        email_public=data.email_public,
        is_email_verified=data.is_email_verified,
        date_of_birth=data.date_of_birth,
        date_of_birth_public=data.date_of_birth_public,
        phone_number=data.phone_number,
        phone_public=data.phone_public,
        social_network=data.social_network,
        social_public=data.social_public,
        is_banned=data.is_banned,
        deletion_scheduled_at=data.deletion_scheduled_at,
        consent_given=data.consent_given,
        consent_date=data.consent_date,
        consent_version=(
            _to_dto_out_consent(data.consent_version) if data.consent_version else None
        ),
        location=(
            _to_dto_out_location(data.location, map_location) if data.location else None
        ),
    )
