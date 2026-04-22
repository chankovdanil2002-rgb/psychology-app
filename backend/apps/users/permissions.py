"""
Кастомные классы прав доступа для ролевой модели.
"""
from rest_framework.permissions import BasePermission


class IsClient(BasePermission):
    """Разрешает доступ только пользователям с ролью клиента."""

    message = 'Access restricted to clients only.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'client'
        )


class IsPsychologist(BasePermission):
    """Разрешает доступ только пользователям с ролью психолога."""

    message = 'Access restricted to psychologists only.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'psychologist'
        )


class IsAdmin(BasePermission):
    """Разрешает доступ только пользователям с ролью администратора."""

    message = 'Access restricted to administrators only.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsProfileComplete(BasePermission):
    """
    Разрешает доступ только если профиль пользователя полностью заполнен.

    Проверяет флаг is_profile_complete на связанном ClientProfile
    или PsychologistProfile в зависимости от роли.
    """

    message = 'You must complete your profile before accessing this resource.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role == 'client':
            profile = getattr(user, 'client_profile', None)
            return profile is not None and profile.is_profile_complete

        if user.role == 'psychologist':
            profile = getattr(user, 'psychologist_profile', None)
            return profile is not None and profile.is_profile_complete

        # Администраторы всегда считаются «заполненными».
        if user.role == 'admin':
            return True

        return False


class IsVerifiedPsychologist(BasePermission):
    """
    Разрешает доступ только психологам, верифицированным администратором.
    """

    message = 'Your account has not been verified yet.'

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.role != 'psychologist':
            return False

        profile = getattr(user, 'psychologist_profile', None)
        return profile is not None and profile.is_verified
