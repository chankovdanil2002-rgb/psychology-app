"""
Сериализаторы для модели ClientProfile.

ClientProfileSerializer  -- сериализатор чтения/записи для редактирования профиля.
ClientProfileDetailSerializer -- сериализатор только для чтения, включающий email пользователя.
"""
from django.utils import timezone
from rest_framework import serializers

from apps.clients.models import ClientProfile
from apps.users.image_utils import uploaded_image_to_data_url


class ClientProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения/записи, используемый, когда клиент смотрит или обновляет собственный профиль.
    Включает email и role из связанной модели User (только чтение), чтобы
    фронтенд-AuthContext мог их получить.
    """

    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    avatar = serializers.ImageField(
        write_only=True,
        required=False,
        allow_empty_file=False,
    )

    class Meta:
        model = ClientProfile
        fields = [
            'id',
            'email',
            'role',
            'first_name',
            'last_name',
            'phone',
            'date_of_birth',
            'avatar',
            'is_profile_complete',
        ]
        read_only_fields = ['email', 'role', 'is_profile_complete']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['avatar'] = instance.avatar or ''
        return data

    def update(self, instance, validated_data):
        avatar_file = validated_data.pop('avatar', None)
        instance = super().update(instance, validated_data)

        if avatar_file is not None:
            instance.avatar = uploaded_image_to_data_url(avatar_file)
            instance.save(update_fields=['avatar'])

        return instance

    def validate_date_of_birth(self, value):
        today = timezone.localdate()
        try:
            latest_allowed_birth_date = today.replace(year=today.year - 14)
        except ValueError:
            latest_allowed_birth_date = today.replace(
                year=today.year - 14,
                day=28,
            )

        if value and value > latest_allowed_birth_date:
            raise serializers.ValidationError(
                'Регистрация доступна клиентам от 14 лет.'
            )
        return value


class ClientProfileDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор только для чтения, добавляющий email пользователя.

    Используется, когда другим частям системы нужно показать информацию о клиенте
    вместе с email привязанного аккаунта.
    """

    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = ClientProfile
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'date_of_birth',
            'avatar',
            'is_profile_complete',
        ]
        read_only_fields = fields
