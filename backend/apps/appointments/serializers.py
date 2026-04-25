"""Сериализаторы для приложения appointments."""
from django.db import transaction
from rest_framework import serializers

from apps.schedule.models import TimeSlot

from .models import Appointment


ACTIVE_APPOINTMENT_STATUSES = (
    Appointment.Status.PENDING,
    Appointment.Status.CONFIRMED,
)


class AppointmentCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания новой записи на прием.

    Проверяет, что тайм-слот существует, свободен и не имеет активной записи.
    Отмененные и отклоненные записи остаются в истории, но не блокируют слот.
    """

    time_slot_id = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True, default='')

    @staticmethod
    def _slot_has_active_appointment(slot):
        return Appointment.objects.filter(
            time_slot=slot,
            status__in=ACTIVE_APPOINTMENT_STATUSES,
        ).exists()

    def validate_time_slot_id(self, value):
        """Проверяет существование и доступность выбранного тайм-слота."""
        try:
            slot = TimeSlot.objects.select_related('psychologist').get(pk=value)
        except TimeSlot.DoesNotExist:
            raise serializers.ValidationError('Время приема не найдено.')

        if not slot.is_available or self._slot_has_active_appointment(slot):
            raise serializers.ValidationError(
                'Это время уже занято. Выберите другой слот.'
            )
        return value

    def validate(self, attrs):
        """Проверяет, что профиль клиента заполнен."""
        request = self.context['request']
        client_profile = getattr(request.user, 'client_profile', None)
        if client_profile is None or not client_profile.is_profile_complete:
            raise serializers.ValidationError(
                'Заполните профиль перед записью на прием.'
            )
        return attrs

    def create(self, validated_data):
        """Создает запись и помечает тайм-слот как занятый."""
        request = self.context['request']

        with transaction.atomic():
            slot = TimeSlot.objects.select_for_update().select_related(
                'psychologist',
            ).get(pk=validated_data['time_slot_id'])

            if not slot.is_available or self._slot_has_active_appointment(slot):
                raise serializers.ValidationError({
                    'time_slot_id': 'Это время уже занято. Выберите другой слот.'
                })

            appointment = Appointment.objects.create(
                client=request.user.client_profile,
                psychologist=slot.psychologist,
                time_slot=slot,
                comment=validated_data.get('comment', ''),
            )

            slot.is_available = False
            slot.save(update_fields=['is_available'])

        return appointment


class AppointmentListSerializer(serializers.ModelSerializer):
    """Короткий сериализатор записи для списков."""

    client_name = serializers.SerializerMethodField()
    psychologist_name = serializers.SerializerMethodField()
    date = serializers.DateField(source='time_slot.date', read_only=True)
    start_time = serializers.TimeField(source='time_slot.start_time', read_only=True)
    end_time = serializers.TimeField(source='time_slot.end_time', read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'client_name',
            'psychologist_name',
            'date',
            'start_time',
            'end_time',
            'status',
            'created_at',
        )
        read_only_fields = fields

    def get_client_name(self, obj):
        return str(obj.client)

    def get_psychologist_name(self, obj):
        return str(obj.psychologist)


class AppointmentDetailSerializer(serializers.ModelSerializer):
    """Подробный сериализатор одной записи."""

    client_name = serializers.SerializerMethodField()
    psychologist_name = serializers.SerializerMethodField()
    psychologist_id = serializers.IntegerField(
        source='psychologist.id', read_only=True
    )
    date = serializers.DateField(source='time_slot.date', read_only=True)
    start_time = serializers.TimeField(source='time_slot.start_time', read_only=True)
    end_time = serializers.TimeField(source='time_slot.end_time', read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id',
            'client_name',
            'psychologist_name',
            'psychologist_id',
            'date',
            'start_time',
            'end_time',
            'status',
            'comment',
            'created_at',
            'updated_at',
        )
        read_only_fields = fields

    def get_client_name(self, obj):
        return str(obj.client)

    def get_psychologist_name(self, obj):
        return str(obj.psychologist)
