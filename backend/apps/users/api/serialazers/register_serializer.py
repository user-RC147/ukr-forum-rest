from rest_framework import serializers

from core.serializers.location_serializer import LocationInSerializer,LocationOutSerializer

class RegisterInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    display_name = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    email = serializers.EmailField()
    referral_code = serializers.UUIDField(default=None, required=False, allow_null=True)
    consent_given = serializers.BooleanField(default=False)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Паролі не збігаються")
        return data

    def validate_consent_given(self, data):
        if data is False:
            raise serializers.ValidationError("Немає погодження")
        return data


class ProfileUpdateInSerializer(serializers.Serializer):
    display_name = serializers.CharField(max_length=100, required=False)

    first_name_public = serializers.BooleanField(required=False)
    last_name_public = serializers.BooleanField(required=False)

    email = serializers.BooleanField(required=False)
    email_public = serializers.BooleanField(required=False)

    date_of_birth = serializers.DateField(required=False)
    date_of_birth_public = serializers.BooleanField(required=False)

    phone_number = serializers.CharField(max_length=50, required=False)
    phone_public = serializers.BooleanField(required=False)

    social_network = serializers.CharField(max_length=50, required=False)
    social_public = serializers.BooleanField(required=False)

    location=LocationInSerializer()
    
