from rest_framework.permissions import BasePermission

from apps.household.models.group import GroupMember


class IsGroupMember(BasePermission):

    """
    Будь-який член групи — viewer, editor, creator.
    Використовується для read-only дій (list, retrieve).
    """
    message="Ви не є членом цієї групи."
    
    def has_object_permission(self, request, view, obj):
        return GroupMember.objects.filter(
            group=obj.group,
            user=request.user,
        ).exists()

class IsGroupEditor(BasePermission):

    """
    Може редагувати — editor або creator.
    Використовується для create, update, partial_update.
    """
    message="Потрібна роль editor або creator."

    def has_object_permission(self,request,view,obj):
        return GroupMember.objects.filter(
            group=obj.group,
            user=request.user,
            role__in=[
                GroupMember.Role.EDITOR,
                GroupMember.Role.CREATOR,
            ],
        ).exists()

class IsGroupCreator(BasePermission):

    """
    Тільки creator — видалення, керування учасниками.
    """
    message = "Потрібна роль creator."

    def has_object_permission(self,request,view,obj):
        return GroupMember.objects.filter(
            group=obj.group,
            user=request.user,
            role=GroupMember.Role.CREATOR,
        ).exists()


class IsOwner(BasePermission):
    """
    Тільки той хто створив об'єкт може його редагувати або видаляти.
    Використовується для глобальних моделей: Market, Product.
    """
    message = "Тільки автор може редагувати цей запис."

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user