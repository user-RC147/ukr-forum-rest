from dataclasses import dataclass


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
