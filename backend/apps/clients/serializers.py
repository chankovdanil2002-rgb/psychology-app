"""
Сериализаторы для модели ClientProfile.

ClientProfileSerializer  -- сериализатор чтения/записи для редактирования профиля.
ClientProfileDetailSerializer -- сериализатор только для чтения, включающий email пользователя.
"""
from rest_framework import serializers

from apps.clients.models import ClientProfile


class ClientProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения/записи, используемый, когда клиент смотрит или обновляет собственный профиль.
    Включает email и role из связанной модели User (только чтение), чтобы
    фронтенд-AuthContext мог их получить.
    """

    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

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
