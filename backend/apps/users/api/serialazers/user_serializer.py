from rest_framework import serializers

from core.serializers.location_serializer import CountrySerializer,RegionSerializer,CitySerializer,LocationInSerializer,Location_id_region_OutSerializer



class ConsentOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    version=serializers.CharField()
    text=serializers.CharField()
    created_at=serializers.DateTimeField()


class UserShortOutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    display_name = serializers.CharField(max_length=100)

class UserPublicOutSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    display_name = serializers.CharField(max_length=100)

    # first_name_public:bool
    # last_name_public:bool

    # email_public:str
    # is_email_verified:bool

    # date_of_birth:datetime
    # date_of_birth_public:bool

    # phone_number:str
    # phone_public:bool

    # social_network:str
    # social_public:bool


class UserPrivatOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    display_name = serializers.CharField(max_length=100)

    first_name=serializers.CharField()
    first_name_public=serializers.BooleanField()

    last_name=serializers.CharField()
    last_name_public=serializers.BooleanField()

    email=serializers.EmailField()
    email_public=serializers.BooleanField()
    is_email_verified=serializers.BooleanField()

    date_of_birth=serializers.DateField(allow_null=True)
    date_of_birth_public=serializers.BooleanField()

    phone_number=serializers.CharField(allow_null=True, allow_blank=True)
    phone_public=serializers.BooleanField()

    social_network=serializers.CharField(allow_null=True, allow_blank=True)
    social_public=serializers.BooleanField()

    is_banned=serializers.BooleanField()

    deletion_scheduled_at=serializers.DateTimeField()

    consent_given=serializers.BooleanField()
    consent_date=serializers.DateTimeField()
    consent_version=ConsentOutSerializer(allow_null=True)

    country_public=serializers.BooleanField()
    region_public=serializers.BooleanField()
    city_public=serializers.BooleanField()

    location=Location_id_region_OutSerializer(allow_null=True)
