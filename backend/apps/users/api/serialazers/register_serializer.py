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

    display_name = serializers.CharField(max_length=100)

    first_name=serializers.CharField(allow_blank=True)
    first_name_public = serializers.BooleanField()

    last_name=serializers.CharField(allow_blank=True)
    last_name_public = serializers.BooleanField()

    email = serializers.EmailField()
    email_public = serializers.BooleanField()

    date_of_birth = serializers.DateField(allow_null=True)
    date_of_birth_public = serializers.BooleanField()

    phone_number = serializers.CharField(max_length=50, allow_blank=True)
    phone_public = serializers.BooleanField()

    social_network = serializers.CharField(max_length=50, allow_blank=True)
    social_public = serializers.BooleanField()

    country_public=serializers.BooleanField()
    region_public=serializers.BooleanField()
    city_public=serializers.BooleanField()

    location=LocationInSerializer()
    
