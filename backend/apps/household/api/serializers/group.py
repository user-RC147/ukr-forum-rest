from rest_framework import serializers

from apps.household.models import Group, GroupMember


class GroupMemberSrializer(serializers.ModelSerializer):
    """
    Серіалізатор учасника групи.
    Використовується всередині GroupSerializer для відображення списку учасників.
    Поле user — read_only, бо змінювати користувача не можна, тільки роль.
    """
    username=serializers.CharField(source='user.username',read_only=True)

    class Meta:
        model=GroupMember
        fields=['id','user','username','role','joined_at']
        read_only_fields=['id','joined_at','username']

class GroupSerializer(serializers.ModelSerializer):

    """
    Серіалізатор групи.
    - members — вкладений список учасників, тільки для читання.
    - created_by — підставляється автоматично з request.user в perform_create.
    """
    members=GroupMemberSrializer(many=True,read_only=True)
    created_by=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Group
        fields=['id','name','created_by','created_at','members']
        read_only_fields=['id','created_at','created_by','members']