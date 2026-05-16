from dataclasses import dataclass

@dataclass
class UserDTO:
    """
    Публічне представлення користувача.
    Використовується іншими модулями — household, тощо.
    Містить тільки те що безпечно показувати.
    """
    id:int
    username:str
    display_name:str
    