from rest_framework import serializers


class ConsentOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    version=serializers.CharField()
    text=serializers.CharField()
    created_at=serializers.DateTimeField()


class CountryOutSerialize(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    code=serializers.CharField()
    flag_emoji=serializers.CharField()
    currency=serializers.CharField()

class RegionOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    country_id=serializers.IntegerField()

class CityOutSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField()
    name_ua=serializers.CharField()
    country_id=serializers.IntegerField()
    region_id=serializers.IntegerField()
    latitude=serializers.DecimalField(max_digits=20, decimal_places=16,allow_null=True)
    longitude=serializers.DecimalField(max_digits=20, decimal_places=16,allow_null=True)



class LocatioOutSerializer(serializers.Serializer):
    country=CountryOutSerialize()
    region=RegionOutSerializer()
    city=CityOutSerializer()



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

    first_name_public=serializers.BooleanField()
    last_name_public=serializers.BooleanField()

    email=serializers.CharField()
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

    location=LocatioOutSerializer(allow_null=True)
