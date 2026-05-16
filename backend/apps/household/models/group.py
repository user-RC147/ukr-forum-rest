from django.db import models
from django.conf import settings


class Group(models.Model):
    name=models.CharField(max_length=100,verbose_name="Назва групи")
    created_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← завжди вказує на активну модель користувача
        on_delete=models.CASCADE,
        related_name="created_groups",
        verbose_name="Створив",
    )
    created_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата створення",
    )

    class Meta:
        db_table = "household_group"
        verbose_name = "Група"
        verbose_name_plural = "Групи"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
    

class GroupMember(models.Model):
    """
    Учасник групи з роллю.
    """
    class Role(models.TextChoices):
        CREATOR = "creator", "Власник"
        EDITOR  = "editor",  "Редактор"
        VIEWER  = "viewer",  "Глядач"
    
    group=models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Група",
    )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← завжди вказує на активну модель користувача
        on_delete=models.CASCADE,
        related_name="group_memberships",
        verbose_name="Користувач",
    )
    role=models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.VIEWER,
        verbose_name="Роль",
    )
    joined_at=models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата приєднання",
    )

    class Meta:
        db_table="household_group_member"
        verbose_name="Учасник групи"
        verbose_name_plural="Учасники групи"
        unique_together=("group","user")

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"