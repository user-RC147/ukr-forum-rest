from rest_framework import serializers




class RegisterInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    display_name=serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField()
    referral_code = serializers.UUIDField(default=None,required=False, allow_null=True)
    consent_given = serializers.BooleanField(default=False)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Паролі не збігаються")
        return data
    
    
    def validate_consent_given(self, data):
        if data is False:
            raise serializers.ValidationError("Немає погодження")
        return data
