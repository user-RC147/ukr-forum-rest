from faulthandler import is_enabled
from django.db import models
from django.conf import settings


# CREATOR = "creator", "Власник"
# EDITOR = "editor", "Редактор"
# VIEWER = "viewer", "Глядач"
class Role(models.Model):
    name = models.CharField(default="viewer", verbose_name="Роль користувача")
    name_ua = models.CharField(
        blank=True, default="", verbose_name="Роль користувача українською"
    )
    is_bool = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name_ua}"


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва групи")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← завжди вказує на активну модель користувача
        on_delete=models.CASCADE,
        related_name="created_groups",
        verbose_name="Створив",
    )
    created_at = models.DateTimeField(
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

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Група",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # ← завжди вказує на активну модель користувача
        on_delete=models.CASCADE,
        related_name="group_memberships",
        verbose_name="Користувач",
    )
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль")

    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата приєднання",
    )

    class Meta:
        db_table = "household_group_member"
        verbose_name = "Учасник групи"
        verbose_name_plural = "Учасники групи"
        unique_together = ("group", "user")

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role.name})"
