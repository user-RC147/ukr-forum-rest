from django.db import transaction

from apps.household.dto.group_dto import CreateGroupInDTO, GroupMemberOutDTO, GroupOutDTO
from apps.household.models.group import Group,GroupMember


class GroupRepo:
    
    
    def create_group(self,dto:CreateGroupInDTO,creator_id:int)->bool:
        
        create_group = Group.objects.create(
            name=dto.name,
            created_by_id=creator_id
        )
        if create_group:
            return True
        # new_create_group=Group.objects.select_related('members').get(id=create_group.id)
        # create_group_dto = GroupOutDTO(
        #     id=new_create_group.id,
        #     name=new_create_group.name,
        #     created_by=new_create_group.created_by_username,
        #     created_at=new_create_group.created_at,
        #     members=GroupMemberOutDTO(
        #         id=new_create_group.members.id,
        #         group_id = new_create_group
        #         user_id=new_create_group.members.user_id,
        #         username=new_create_group.members.username,
        #         role=new_create_group.members.role,
        #         joined_at=new_create_group.members.joined_at
        #     ) 

        # )