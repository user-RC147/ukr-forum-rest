from rest_framework import serializers


class ConfirmEmailInSerializer(serializers.Serializer):
    token = serializers.CharField()
