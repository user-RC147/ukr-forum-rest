from typing import Sequence
from apps.geo import repositories
from apps.household.dto import CreateGroupInDTO,GroupOutDTO
from apps.household.repositories import GroupRepo
from apps.household.selectors import GroupSelector

from apps.users.contracts.user_contract import get_user_contract  


class GroupService:
    """
    Сервіс для управління бізнес-логікою груп користувачів.
    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._group_repo=GroupRepo()
        self._group_selector= GroupSelector()
        self._get_user_contract = get_user_contract()

    def get_user_in_group_exists(self,user_id:int)->bool:
        user = self._get_user_contract.get(user_id=user_id)
        return user




    def get_all_list(self,user_id:int)->Sequence[GroupOutDTO]:
        """
        Отримання переліку груп, у яких користувач є учасником.
        СТРОГО ЧЕРЕЗ СЕЛЕКТОР (Шар читання).
        """
        self.get_user_in_group_exists(user_id)

        return self._group_selector.get_groups_for_user(user_id=user_id)

    def create_new_group(self,dto:CreateGroupInDTO,creator_id:int)->int:
        """
        Бізнес-логіка створення нової групи.
        Приймає вхідне DTO, передає дані в репозиторій та повертає ID створеної групи.
        """
        # Тут за потреби можна додати бізнес-перевірки: 
        # наприклад, чи не перевищив користувач ліміт на створення груп.
        group=self._group_repo.create_group_with_creator(
            name=dto.name,
            creator_id=creator_id
        )

        return group.id