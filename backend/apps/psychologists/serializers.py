"""
Сериализаторы для модели PsychologistProfile.

Предоставляет сериализаторы под разные сценарии:
  - PsychologistProfileSerializer: редактирование своего профиля
  - PsychologistListSerializer: публичный каталог
  - PsychologistDetailSerializer: полная публичная страница психолога
  - AdminPsychologistListSerializer: список команды для админа
  - AdminPsychologistCreateSerializer: создание психологов админом
"""
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from apps.psychologists.models import PsychologistProfile
from apps.users.models import User


class PsychologistProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для просмотра и редактирования психологом собственного профиля.

    Включает email и role из связанной модели User (только чтение), чтобы
    фронтенд-AuthContext мог их получить.
    """

    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = PsychologistProfile
        fields = [
            'id',
            'email',
            'role',
            'first_name',
            'last_name',
            'patronymic',
            'phone',
            'photo',
            'experience_years',
            'education',
            'bio',
            'price',
            'diploma_scan',
            'is_verified',
            'verified_at',
            'is_profile_complete',
        ]
        read_only_fields = ['email', 'role', 'is_verified', 'verified_at']


class PsychologistListSerializer(serializers.ModelSerializer):
    """
    Компактный сериализатор для публичного каталога психологов.

    Включает вычисляемые поля рейтинга и количества отзывов, а также
    вложенный список названий специализаций.
    """

    full_name = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)

    class Meta:
        model = PsychologistProfile
        fields = [
            'id',
            'full_name',
            'photo',
            'experience_years',
            'bio',
            'price',
            'specializations',
            'average_rating',
            'total_reviews',
        ]

    def get_full_name(self, obj):
        """Возвращает полное ФИО психолога."""
        parts = [obj.last_name, obj.first_name]
        if obj.patronymic:
            parts.append(obj.patronymic)
        return ' '.join(p for p in parts if p)

    def get_specializations(self, obj):
        """Возвращает список названий специализаций, привязанных к психологу."""
        return list(
            obj.specializations.values_list('name', flat=True)
        )


class PsychologistDetailSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для страницы деталей психолога.

    Включает все публичные поля, специализации и отзывы.
    """

    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    specializations = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = PsychologistProfile
        fields = [
            'id',
            'full_name',
            'email',
            'phone',
            'photo',
            'experience_years',
            'education',
            'bio',
            'price',
            'specializations',
            'average_rating',
            'total_reviews',
            'reviews',
        ]

    def get_full_name(self, obj):
        """Возвращает полное ФИО психолога."""
        parts = [obj.last_name, obj.first_name]
        if obj.patronymic:
            parts.append(obj.patronymic)
        return ' '.join(p for p in parts if p)

    def get_specializations(self, obj):
        """Возвращает список словарей специализаций (id, name, slug)."""
        return list(
            obj.specializations.values('id', 'name', 'slug')
        )

    def get_reviews(self, obj):
        """Возвращает список отзывов по завершённым приёмам."""
        from apps.reviews.serializers import ReviewSerializer

        reviews_qs = []
        for appointment in obj.appointments.filter(
            status='completed', review__isnull=False
        ).select_related('review', 'client__user'):
            reviews_qs.append(appointment.review)

        return ReviewSerializer(reviews_qs, many=True).data


class AdminPsychologistListSerializer(serializers.ModelSerializer):
    """Сериализатор для администраторов для просмотра списка психологов."""

    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(
        source='user.date_joined',
        read_only=True,
    )
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = PsychologistProfile
        fields = [
            'id',
            'full_name',
            'email',
            'date_joined',
            'is_active',
            'is_verified',
            'is_profile_complete',
        ]

    def get_full_name(self, obj):
        """Возвращает полное ФИО психолога."""
        parts = [obj.last_name, obj.first_name]
        if obj.patronymic:
            parts.append(obj.patronymic)
        return ' '.join(p for p in parts if p)


class AdminPsychologistCreateSerializer(serializers.Serializer):
    """Сериализатор для создания аккаунтов психологов администратором."""

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
    )
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    patronymic = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
    )

    def validate_email(self, value):
        """Проверяет уникальность email."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email

    def validate_password(self, value):
        """Валидирует пароль встроенными валидаторами Django."""
        validate_password(value)
        return value

    def create(self, validated_data):
        """Создаёт активный, верифицированный аккаунт психолога."""
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=User.Role.PSYCHOLOGIST,
            is_active=True,
        )

        profile, _ = PsychologistProfile.objects.get_or_create(user=user)
        profile.first_name = validated_data['first_name']
        profile.last_name = validated_data['last_name']
        profile.patronymic = validated_data.get('patronymic', '')
        profile.is_verified = True
        profile.verified_at = timezone.now()
        profile.save()
        return profile
