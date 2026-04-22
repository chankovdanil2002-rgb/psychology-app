"""
Конфигурация Django admin для моделей User и EmailConfirmationToken.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import EmailConfirmationToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ-интерфейс для кастомной модели User."""

    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)

    # Поля, отображаемые на странице деталей/редактирования пользователя.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Role', {'fields': ('role',)}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, отображаемые на странице создания пользователя.
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'role',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                ),
            },
        ),
    )


@admin.register(EmailConfirmationToken)
class EmailConfirmationTokenAdmin(admin.ModelAdmin):
    """Админ-интерфейс для токенов подтверждения email."""

    list_display = ('user', 'token', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at')
    ordering = ('-created_at',)
