from rest_framework import serializers

class PasswordResetRequestInSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmInSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    new_password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError("Паролі не збігаються")
        return data