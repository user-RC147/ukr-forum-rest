from email.headerregistry import Group
from apps.geo import repositories
from apps.household.dto import CreateGroupInDTO, GroupOutDTO
from apps.household.dto.group_dto import Group_id_user_OutDTO
from apps.household.dto.user_dto import UserOutDTO
from apps.household.repositories import GroupRepo
from apps.household.selectors import GroupSelector

from apps.users.contracts.user_contract import get_user_contract


class GroupService:
    """
    Сервіс для управління бізнес-логікою груп користувачів.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._group_repo = GroupRepo()
        self._group_selector = GroupSelector()
        self._get_user_contract = get_user_contract()
        self._selector = GroupSelector()
        self._repository = GroupRepo()

    def get_user_in_group_exists(self) -> bool: ...

    # =================================================
    def _to_user_out(self, data, users_map) -> UserOutDTO:

        return UserOutDTO(
            id=users_map[data.created_by_id].id,
            username=users_map[data.created_by_id].username,
            display_name=users_map[data.created_by_id].display_name,
        )

    def _to_group_out(self, data: Group_id_user_OutDTO, users_map) -> GroupOutDTO:
        return GroupOutDTO(
            id=data.id,
            name=data.name,
            created_by=self._to_user_out(data, users_map),
            created_at=data.created_at,
            members=data.members,
        )

    # =================================================

    def get_all_group_member_by_user(self, user_id: int):

        if self._get_user_contract.get(user_id):
            group_members = self._selector.get_all_group_by_user(user_id=user_id)

            user_ids = list(
                {member.user_id for group in group_members for member in group.members}
            )
            users_map = self._get_user_contract.get_many(user_ids)

            return [
                self._to_group_out(group_member, users_map=users_map)
                for group_member in group_members
            ]

    def create_group(self, dto: CreateGroupInDTO, creator_id: int) -> bool:
        # перевірка корстувача
        if not self._selector.get_group_by_name(dto) and self._get_user_contract.get(creator_id):
            return self._repository.create_group(dto=dto, creator_id=creator_id)
      