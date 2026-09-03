from rest_framework import serializers

from apps.users.api.serializers.user_serializer import UserShortOutSerializer



class ArticleOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    date_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    date_edit = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    created_by = UserShortOutSerializer()


class ArticleInSerializer(serializers.Serializer):
    ...