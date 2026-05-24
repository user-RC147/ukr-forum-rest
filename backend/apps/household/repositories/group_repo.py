from django.db import transaction

from apps.household.models.group import Group,GroupMember


class GroupRepo:
    """
    Репозиторій для роботи з базою даних груп та їх учасників.
    Включає лише чисті операції запису та маніпуляції ORM-моделями.
    """
    def create_group_with_creator(self,name:str,creator_id:int)->Group:
        """
        Створює групу та автоматично додає користувача як CREATOR.
        Операція обгорнута в atomic транзакцію для безпеки даних.
        """
        with transaction.atomic():
            # 1. Створюємо саму групу
            group=Group.objects.create(
                name=name,
                created_by_id=creator_id
            )

            # 2. Одразу створюємо запис учасника з роллю Власника (creator)
            GroupMember.objects.create(
                group=group,
                user_id=creator_id,
                role=GroupMember.Role.CREATOR
            )

            return group