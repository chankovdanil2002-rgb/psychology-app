"""Сериализаторы для приложения appointments."""
from rest_framework import serializers

from apps.schedule.models import TimeSlot

from .models import Appointment


class AppointmentCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания новой записи на приём.

    Проверяет, что тайм-слот существует и свободен, а профиль клиента заполнен.
    """

    time_slot_id = serializers.IntegerField()
    comment = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_time_slot_id(self, value):
        """Проверяет существование и доступность тайм-слота."""
        try:
            slot = TimeSlot.objects.select_related('psychologist').get(pk=value)
        except TimeSlot.DoesNotExist:
            raise serializers.ValidationError('Time slot not found.')

        if not slot.is_available:
            raise serializers.ValidationError(
                'This time slot is no longer available.'
            )
        return value

    def validate(self, attrs):
        """Проверяет, что профиль клиента заполнен."""
        request = self.context['request']
        client_profile = getattr(request.user, 'client_profile', None)
        if client_profile is None or not client_profile.is_profile_complete:
            raise serializers.ValidationError(
                'You must complete your profile before booking an appointment.'
            )
        return attrs

    def create(self, validated_data):
        """Создаёт запись и помечает тайм-слот как занятый."""
        request = self.context['request']
        slot = TimeSlot.objects.select_related('psychologist').get(
            pk=validated_data['time_slot_id'],
        )

        appointment = Appointment.objects.create(
            client=request.user.client_profile,
            psychologist=slot.psychologist,
            time_slot=slot,
            comment=validated_data.get('comment', ''),
        )

        # Помечаем слот как занятый.
        slot.is_available = False
        slot.save(update_fields=['is_available'])

        return appointment


class AppointmentListSerializer(serializers.ModelSerializer):
    """Компактный сериализатор для списка записей (только чтение)."""

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
    """Подробный сериализатор одной записи (только чтение)."""

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
