"""Сериализаторы для приложения schedule."""
import datetime

from rest_framework import serializers

from .models import TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    """Сериализатор чтения TimeSlot."""

    psychologist_id = serializers.IntegerField(source='psychologist.id', read_only=True)

    class Meta:
        model = TimeSlot
        fields = (
            'id',
            'psychologist_id',
            'date',
            'start_time',
            'end_time',
            'is_available',
        )
        read_only_fields = fields


class TimeSlotCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания одного тайм-слота.

    Проверяет, что end_time > start_time, а дата не в прошлом.
    Психолог устанавливается автоматически из аутентифицированного пользователя.
    """

    class Meta:
        model = TimeSlot
        fields = ('id', 'date', 'start_time', 'end_time')
        read_only_fields = ('id',)

    def validate_date(self, value):
        """Проверяет, что дата — сегодня или в будущем."""
        if value < datetime.date.today():
            raise serializers.ValidationError(
                'Cannot create time slots in the past.'
            )
        return value

    def validate(self, attrs):
        """Проверяет, что end_time > start_time."""
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError(
                {'end_time': 'End time must be after start time.'}
            )
        return attrs

    def create(self, validated_data):
        """Подставляет профиль психолога из пользователя запроса."""
        request = self.context['request']
        validated_data['psychologist'] = request.user.psychologist_profile
        return super().create(validated_data)


class BulkTimeSlotCreateSerializer(serializers.Serializer):
    """
    Сериализатор массового создания тайм-слотов в диапазоне дат.

    Создаёт по одному слоту на каждый подходящий день недели между date_from
    и date_to (включительно) с одинаковыми start_time / end_time.
    """

    date_from = serializers.DateField()
    date_to = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    weekdays = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        help_text='Список номеров дней недели (0=понедельник .. 6=воскресенье).',
    )

    def validate_date_from(self, value):
        """Проверяет, что date_from — сегодня или в будущем."""
        if value < datetime.date.today():
            raise serializers.ValidationError(
                'Start date cannot be in the past.'
            )
        return value

    def validate(self, attrs):
        """Кросс-полевая валидация."""
        if attrs['date_to'] < attrs['date_from']:
            raise serializers.ValidationError(
                {'date_to': 'End date must be on or after start date.'}
            )
        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError(
                {'end_time': 'End time must be after start time.'}
            )
        if not attrs['weekdays']:
            raise serializers.ValidationError(
                {'weekdays': 'At least one weekday must be selected.'}
            )
        return attrs

    def create(self, validated_data):
        """
        Создаёт экземпляры TimeSlot для каждого подходящего дня недели в диапазоне.

        Существующие слоты (того же психолога, даты и start_time) молча
        пропускаются через ignore_conflicts.
        """
        request = self.context['request']
        psychologist = request.user.psychologist_profile

        date_from = validated_data['date_from']
        date_to = validated_data['date_to']
        start_time = validated_data['start_time']
        end_time = validated_data['end_time']
        weekdays = set(validated_data['weekdays'])

        slots = []
        current = date_from
        while current <= date_to:
            if current.weekday() in weekdays:
                slots.append(
                    TimeSlot(
                        psychologist=psychologist,
                        date=current,
                        start_time=start_time,
                        end_time=end_time,
                    )
                )
            current += datetime.timedelta(days=1)

        created = TimeSlot.objects.bulk_create(slots, ignore_conflicts=True)
        return created
