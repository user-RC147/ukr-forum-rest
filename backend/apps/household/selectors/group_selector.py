from apps.household.dto.group_dto import Group_Id_Name_InDTO,Group_id_user_OutDTO, GroupMember_id_user_OutDTO, GroupOutDTO,CreateGroupInDTO,RoleOutDTO
from apps.household.models.group import Group, GroupMember, Role
from django.db.models import Q

from core.func_print import prt

class GroupSelector:

    # def get_all_group(self):
    #   group_all=Group.objects.all()
    #   return group_all

    def get_group_by_name(self,dto:CreateGroupInDTO)->bool:            
        return Group.objects.filter(name=dto.name).exists()

    def get_all_group_by_user(self, dto:Group_Id_Name_InDTO, user_id: int):
        # Шукаємо зв'язки учасників і підвантажуємо групу та роль, щоб не було зайвих запитів
        #Group.objects.filter(members__user_id=user_id).prefetch_related("members__user", "members__role" )

        #groups = Group.objects.filter(members__user_id=user_id).prefetch_related("members__role" )
        
        if dto.id:
            groups = (Group.objects.filter(
                Q(id=dto.id) &
                   ( Q(created_by_id=user_id) |
                    Q(members__user_id=user_id))
                )
                .distinct()
                .prefetch_related(
                    "members__role"
                )
            )        
        else:
            groups = (Group.objects.filter(
                    Q(created_by_id=user_id) |
                    Q(members__user_id=user_id)
                )
                .distinct()
                .prefetch_related(
                    "members__role"
                )
            )
        
        groups_dto = [_to_group_id_user_out(group_obj) for group_obj in groups]
        
        return groups_dto

#==========================================
def _to_role(data:Role)->RoleOutDTO:
    return RoleOutDTO(
        id=data.id,
        name=data.name,
        name_ua=data.name_ua,
        is_bool=data.is_bool
    )


def _to_group_member_out(data:GroupMember)->GroupMember_id_user_OutDTO:
    return GroupMember_id_user_OutDTO(
        id=data.id,
        group_id=data.group_id,
        user_id=data.user_id,
        role=_to_role(data.role),
        joined_at= data.joined_at
    )

def _to_group_id_user_out(data:Group)->Group_id_user_OutDTO:
    return Group_id_user_OutDTO(
        id=data.id,
        name=data.name,
        created_by_id=data.created_by_id,
        created_at=data.created_at,
        members=[_to_group_member_out(member)for member in data.members.all()]
    )

#==========================================