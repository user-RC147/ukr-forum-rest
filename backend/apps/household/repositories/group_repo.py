from django.db import transaction

from apps.household.dto.group_dto import (
    CreateGroupInDTO,
    GroupMemberOutDTO,
    GroupOutDTO,
)
from apps.household.dto.user_dto import User_Id_OutDTO, UserOutDTO
from apps.household.models.group import Group, GroupMember


class GroupRepo:

    def create_group(self, dto: CreateGroupInDTO, creator_user: UserOutDTO) -> GroupOutDTO:

        create_group = Group.objects.create(
            name=dto.name, 
            created_by_id=creator_user.id
        )

        create_group_dto = GroupOutDTO(
            id=create_group.id,
            name=create_group.name,
            created_by=creator_user,
            created_at=create_group.created_at,
            members=None
        )
        return create_group_dto
