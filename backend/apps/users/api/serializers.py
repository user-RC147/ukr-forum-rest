from rest_framework import serializers

from apps.users.dto import (
    RegisterDTO,
    ProfileUpdateDTO,
    PasswordResetConfirmDTO,
    ChangePasswordDTO,
    LocationUpdateDTO
)


class UserRegisterSerializer(serializers.Serializer):
    """
    Валідує дані реєстрації і перетворює в RegisterDTO.
    
    Чому Serializer а не ModelSerializer?
    ModelSerializer прив'язаний до моделі — він сам вирішує
    що валідувати і як зберігати. Нам це не потрібно —
    збереженням займається сервіс. Тому чистий Serializer.
    """
    username  = serializers.CharField(max_length=150)
    email     = serializers.EmailField()
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    country   = serializers.CharField(required=False, allow_blank=True, default=None)
    region    = serializers.CharField(required=False, allow_blank=True, default=None)
    city      = serializers.CharField(required=False, allow_blank=True, default=None)

    def validate(self, attrs):
        """
        validate() викликається після перевірки кожного поля окремо.
        Тут перевіряємо логіку яка стосується кількох полів одночасно.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password2": "Паролі не співпадають."}
            )
        return attrs

    def to_dto(self) -> RegisterDTO:
        """
        Перетворює валідовані дані в DTO.
        Викликається у view після is_valid().
        """
        data = self.validated_data
        return RegisterDTO(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city'),
        )


class UserProfileSerializer(serializers.Serializer):
    """
    Валідує дані оновлення профілю і перетворює в ProfileUpdateDTO.
    Всі поля необов'язкові — користувач може оновити тільки частину.
    """
    # display_name   = serializers.CharField(required=False, allow_blank=True)
    # phone_number   = serializers.CharField(required=False, allow_blank=True)
    # age            = serializers.IntegerField(required=False, min_value=0, max_value=120,allow_null=True,)
    # social_network = serializers.CharField(required=False, allow_blank=True)
    # consent_given  = serializers.BooleanField(required=False)

    display_name   = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number   = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    age            = serializers.IntegerField(required=False, min_value=0, max_value=120, allow_null=True)
    social_network = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    consent_given  = serializers.BooleanField(required=False)

    def to_dto(self) -> ProfileUpdateDTO:
        data = self.validated_data
        return ProfileUpdateDTO(
            display_name=data.get('display_name'),
            phone_number=data.get('phone_number'),
            age=data.get('age'),
            social_network=data.get('social_network'),
            consent_given=data.get('consent_given'),
        )


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Тільки email — для запиту відновлення паролю.
    Немає to_dto() бо сервіс приймає просто рядок email.
    """
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Валідує uid, token і новий пароль.
    """
    uid          = serializers.CharField()
    token        = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password2": "Паролі не співпадають."}
            )
        return attrs

    def to_dto(self) -> PasswordResetConfirmDTO:
        data = self.validated_data
        return PasswordResetConfirmDTO(
            uid=data['uid'],
            token=data['token'],
            new_password=data['new_password'],
        )


class ChangePasswordSerializer(serializers.Serializer):
    """
    Валідує старий і новий пароль для зміни паролю.
    """
    old_password  = serializers.CharField(write_only=True, min_length=8)
    new_password  = serializers.CharField(write_only=True, min_length=8)
    new_password2 = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password2": "Паролі не співпадають."}
            )
        return attrs

    def to_dto(self) -> ChangePasswordDTO:
        data = self.validated_data
        return ChangePasswordDTO(
            old_password=data['old_password'],
            new_password=data['new_password'],
        )
    

class LocationUpdateSerializer(serializers.Serializer):
    """
    Валідує id країни, регіону, міста з зовнішнього API.
    """
    country_id = serializers.IntegerField(required=False, allow_null=True)
    region_id  = serializers.IntegerField(required=False, allow_null=True)
    city_id    = serializers.IntegerField(required=False, allow_null=True)

    def to_dto(self) -> LocationUpdateDTO:
        data = self.validated_data
        return LocationUpdateDTO(
            country_id=data.get('country_id'),
            region_id=data.get('region_id'),
            city_id=data.get('city_id'),
        )



