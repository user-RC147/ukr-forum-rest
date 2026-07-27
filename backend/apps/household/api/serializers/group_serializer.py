from rest_framework import serializers

from apps.household.api.serializers.user_serializer import UserOutSerializer
from apps.household.dto.group_dto import CreateGroupInDTO



class RoleSerialiser(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()

class GroupSerialiser(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    created_by=serializers.CharField()
    created_at=serializers.DateTimeField(format="%Y-%m-%d")


class GroupMemberOutSerializer(serializers.Serializer):
    """
    Серіалізатор для відображення учасника групи.
    Працює виключно з об'єктами GroupMemberOutDTO.
    """
    id = serializers.IntegerField(read_only=True)
    group_id=serializers.IntegerField(read_only=True)   
    user = UserOutSerializer()
    role = RoleSerialiser()
    joined_at = serializers.DateTimeField(format="%Y-%m-%d")


class GroupOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    created_by=UserOutSerializer()
    members = GroupMemberOutSerializer(many=True)
    created_at=serializers.DateTimeField(format="%Y-%m-%d")



# class CreateGroupInSerializer(serializers.Serializer):
#     name=serializers.CharField()
    

class Group_Id_InSerializer(serializers.Serializer):
    group_id=serializers.IntegerField(required=False,
    allow_null=True,)


class CreateGroupInSerializer(serializers.Serializer):
    name=serializers.CharField()