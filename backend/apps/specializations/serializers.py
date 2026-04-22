"""Сериализаторы для приложения specializations."""
from django.db import models
from django.db.models import Count
from rest_framework import serializers

from .models import Specialization


class SpecializationSerializer(serializers.ModelSerializer):
    """
    Сериализатор чтения Specialization.

    Включает вычисляемое поле ``psychologist_count``, показывающее,
    сколько верифицированных психологов имеют эту специализацию.
    """

    psychologist_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Specialization
        fields = ('id', 'name', 'slug', 'description', 'icon', 'psychologist_count')
        read_only_fields = fields

    @staticmethod
    def setup_eager_loading(queryset):
        """Добавляет аннотацию psychologist_count к queryset."""
        return queryset.annotate(
            psychologist_count=Count(
                'psychologist_specializations',
                filter=models.Q(
                    psychologist_specializations__psychologist__is_verified=True,
                    psychologist_specializations__psychologist__is_profile_complete=True,
                ),
            ),
        )
