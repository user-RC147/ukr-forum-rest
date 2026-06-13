from apps.household.models.group import GroupMember

from typing import Sequence
from django.db.models import Prefetch
from apps.household.models.group import Group, GroupMember
from apps.household.dto.group_dto import GroupOutDTO, GroupMemberOutDTO


class GroupSelector:
    """
    Центральний селектор для перевірки прав доступу користувачів у групах.
    Використовується як "вхідна охорона" перед виконанням дій.
    """

    def has_write_access_to_asset(self,user_id:int,asset_id:int)->bool:
       
        """
        Перевірка на внесення змін (Створення чеків, додавання товарів).
        Дозволено ТІЛЬКИ для CREATOR та EDITOR.
        """
        # Пояснення дії: Швидким SQL-запитом EXISTS перевіряємо ланцюжок зв'язків.
        # Шукаємо в таблиці GroupMember рядок, де:
        # 1. user_id дорівнює нашому поточному користувачу
        # 2. Група цього учасника містить вказаний Asset (group__assets__id)
        # 3. Роль користувача дозволяє редагування (Власник або Редактор)
        access=GroupMember.objects.filter(
            user_id=user_id,
            group__assets__id=asset_id,
            role__in=[GroupMember.Role.CREATOR,GroupMember.Role.EDITOR]
        ).exists()

        return access
    
    def has_read_access_to_asset(self,user_id:int,asset_id:int)->bool:
       
        """
        Перевірка на перегляд (Історія витрат, аналітика магазинів).
        Дозволено ВСІМ учасникам групи (CREATOR, EDITOR, а також VIEWER).
        """
        # Пояснення дії: Тут ми перевіряємо, чи юзер взагалі є в цій групі.
        # Оскільки CREATOR, EDITOR і VIEWER є легальними учасниками, 
        # ми просто перевіряємо сам факт членства для цього об'єкта (Asset).
        access=GroupMember.objects.filter(
            user_id=user_id,
            group__assets__id=asset_id
        ).exists()
        
        return access

    def get_groups_for_user(self, user_id: int) -> Sequence[GroupOutDTO]:
        """
        Отримує список усіх груп, у яких користувач є учасником.
        Повертає послідовність (Sequence) об'єктів GroupOutDTO з вкладеними учасниками.
        """
        # 1. Оптимізуємо запит: заздалегідь завантажуємо всіх учасників (members) 
        # разом з їхніми username через select_related, щоб уникнути N+1 запитів у циклі.
        members_prefetch = Prefetch(
            'members',
            queryset=GroupMember.objects.select_related('user')
        )

        # 2. Шукаємо групи, де поточний user_id є серед учасників.
        # select_related('created_by') підтягує автора групи одним SQL-запитом.
        groups_queryset = Group.objects.filter(
            members__user_id=user_id
        ).select_related('created_by').prefetch_related(members_prefetch).distinct()

        result = []

        # 3. Мапимо ORM-моделі у чисті DTO структури
        for group in groups_queryset:
            
            # Збираємо список учасників для конкретної групи у GroupMemberOutDTO
            dto_members = [
                GroupMemberOutDTO(
                    id=member.id,
                    user_id=member.user_id,
                    username=member.user.username,  # Дістається з select_related без дод. запиту
                    role=member.role,
                    joined_at=member.joined_at
                )
                for member in group.members.all()
            ]

            # Збираємо саму групу у GroupOutDTO
            group_dto = GroupOutDTO(
                id=group.id,
                name=group.name,
                created_by_username=group.created_by.username,
                created_at=group.created_at,
                members=dto_members
            )
            result.append(group_dto)

        return result