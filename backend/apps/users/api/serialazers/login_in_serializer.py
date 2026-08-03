#login_in_serializer.py
from rest_framework import serializers


class LoginInSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(write_only=True,style={'input_type': 'password'})