from dataclasses import dataclass

@dataclass(frozen=True)
class UserShortOut:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """
    id:int
    username:str
    display_name:str



@dataclass(frozen=True)
class UserOutDTO:
    username
    display_name

    first_name_public
    last_name_public

    email_public
    is_email_verified

    date_of_birth
    date_of_birth_public

    phone_number
    phone_public

    social_network
    social_public

    is_banned

    deletion_scheduled_at

    consent_given
    consent_date
    consent_version
