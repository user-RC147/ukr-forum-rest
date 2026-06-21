
from apps.users.dto.user import UserDTO
from apps.users.models import CustomUser


class UserService:
    """
    Публічний сервіс users модуля.
    Використовується іншими модулями для отримання даних користувача.
    """

    def get_user(self,user_id:int)->UserDTO:

        u=CustomUser.objects.get(id=user_id)
        return UserDTO(
            id=u.id,
            username=u.username,
            display_name=u.get_public_name(),
        )


    def get_users(self, ids: list[int]) -> dict[int, UserDTO]:
        if not ids:
            return {}
            
        data = CustomUser.objects.filter(id__in=ids)

        return {d.id: _to_dto(d) for d in data}

def _to_dto(data) -> UserDTO:
    return UserDTO(id=data.id, username=data.username, display_name=data.get_public_name())

user_service = UserService()
