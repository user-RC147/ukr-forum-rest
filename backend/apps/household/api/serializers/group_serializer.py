from rest_framework import serializers

from apps.household.dto.group_dto import CreateGroupInDTO


class GroupMemberOutSerializer(serializers.Serializer):
    """
    Серіалізатор для відображення учасника групи.
    Працює виключно з об'єктами GroupMemberOutDTO.
    """
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)


class GroupOutSerializer(serializers.Serializer):
    """
    Головний серіалізатор для відображення групи та її учасників.
    Працює виключно з об'єктами GroupOutDTO.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    created_by_username = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    # Вкладений список учасників, який автоматично мапиться з масиву DTO
    members = GroupMemberOutSerializer(many=True, read_only=True)

class CreateGroupInSerializer(serializers.Serializer):
    """
    Вхідний валідатор для створення нової групи.
    Приймає сирі дані з HTTP-запиту (POST).
    """

    name=serializers.CharField(
        max_length=100,
        allow_blank=False,
        help_text="Назва нової групи (наприклад, 'Моя сім'я')"
    )

    def to_dto(self)->CreateGroupInDTO:
        """
        Конвертує перевірені дані (validated_data) у чисте вхідне DTO.
        """
        data=self.validated_data
        new_group=CreateGroupInDTO(
            name=data['name']
        )
        return  new_group