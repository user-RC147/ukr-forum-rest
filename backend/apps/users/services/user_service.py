from typing import Optional

from apps.users.models import CustomUser
from apps.users.dto.user import UserDTO


class UserService:
    """
    Публічний сервіс users модуля.
    Використовується іншими модулями для отримання даних користувача.
    """

    def get_user(self,user_id:int)->Optional[UserDTO]:
        try:
            u=CustomUser.objects.get(id=user_id)
            return UserDTO(
                id=u.id,
                username=u.username,
                display_name=u.get_public_name(),
            )
        except CustomUser.DoesNotExist:
            return None
        

    def get_users(self, ids: list[int]) -> list[UserDTO]:
        if not ids:
            return []
        
        return [
            UserDTO(
                id=u.id,
                username=u.username,
                display_name=u.get_public_name(),
            )
            for u in CustomUser.objects.filter(id__in=ids)
        ]
    
user_service = UserService()