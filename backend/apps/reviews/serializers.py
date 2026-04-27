"""Сериализаторы для приложения reviews."""
from rest_framework import serializers

from apps.appointments.models import Appointment

from .models import Review


class ReviewCreateSerializer(serializers.Serializer):
    """
    Сериализатор создания нового отзыва.

    Проверяет, что запись завершена, принадлежит текущему клиенту и
    к ней ещё не оставлен отзыв.
    """

    appointment_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    text = serializers.CharField()

    def validate_appointment_id(self, value):
        """Проверяет существование записи, её завершённость и отсутствие отзыва."""
        request = self.context['request']

        try:
            appointment = Appointment.objects.select_related(
                'client', 'client__user',
            ).get(pk=value)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError('Запись не найдена.')

        if appointment.client.user != request.user:
            raise serializers.ValidationError(
                'Вы можете оставить отзыв только к своей записи.'
            )

        if appointment.status != Appointment.Status.COMPLETED:
            raise serializers.ValidationError(
                'Отзыв можно оставить только к завершённым записям.'
            )

        if hasattr(appointment, 'review'):
            raise serializers.ValidationError(
                'Отзыв к этой записи уже существует.'
            )

        return value

    def create(self, validated_data):
        """Создаёт отзыв, привязанный к записи."""
        return Review.objects.create(
            appointment_id=validated_data['appointment_id'],
            rating=validated_data['rating'],
            text=validated_data['text'],
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор чтения отзыва с именем клиента и датой."""

    client_name = serializers.SerializerMethodField()
    date = serializers.DateField(source='appointment.time_slot.date', read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'appointment_id',
            'client_name',
            'rating',
            'text',
            'date',
            'created_at',
        )
        read_only_fields = fields

    def get_client_name(self, obj):
        return str(obj.appointment.client)
