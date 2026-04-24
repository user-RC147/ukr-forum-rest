from rest_framework import serializers
from apps.users.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    # write_only=True — пароль приймаємо але ніколи не повертаємо у відповіді
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # create_user — вбудований метод Django який хешує пароль
        # НЕ можна використовувати звичайний create() — пароль збережеться як текст!
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    # Цей серіалайзер для читання профілю — більше полів
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'display_name', 'email',
            'phone_number', 'social_network', 'age',
            'consent_given', 'is_banned',
        ]
        # email і is_banned можна тільки читати, не змінювати через API
        read_only_fields = ['email', 'is_banned']