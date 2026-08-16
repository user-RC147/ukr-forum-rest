from .user_dto import UserShortOutDTO,UserFullOutDTO,UserPublicOutDTO,ProfilUserUpdateInDTO

def _to_dto_user_in(data)->ProfilUserUpdateInDTO:
    return ProfilUserUpdateInDTO(
        username=data.get("display_name"),
        display_name=data.get("display_name"),

        first_name_public=data.get("first_name_public"),
        last_name_public=data.get("last_name_public"),

        email=data.get('email'),
        email_public=data.get("email_public"),

        date_of_birth=data.get("date_of_birth"),
        date_of_birth_public=data.get("date_of_birth_public"),

        phone_number=data.get("phone_number"),
        phone_public=data.get("phone_public"),

        social_network=data.get("social_network"),
        social_public=data.get("social_public"),
        
        location=data.get('location'),
    )

def _to_dto_short_user_out(data)->UserShortOutDTO:
    return UserShortOutDTO(
        id=data.id,
        username=data.username,
        display_name=data.display_name
    )

def _to_dto_user_out(data)->UserPublicOutDTO:
    return UserPublicOutDTO(
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
        location=data.location,
    )