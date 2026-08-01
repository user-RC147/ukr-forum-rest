from apps.users.dto.user_dto import UserOutDTO
from apps.users.selectors.user_selector import UserSelector


class UserService:

    def __init__(self):
        self._selector = UserSelector()

    def get_all_user(self) -> list[UserOutDTO]:
        return self._selector.get_all_users()
