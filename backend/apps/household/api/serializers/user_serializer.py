from rest_framework import serializers


class UserOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    display_name = serializers.CharField()
