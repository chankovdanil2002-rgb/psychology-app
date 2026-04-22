"""
Django-filter FilterSet для каталога психологов.

Поддерживает фильтрацию по slug специализации, диапазону цены и статусу верификации.
"""
import django_filters

from apps.psychologists.models import PsychologistProfile


class PsychologistFilter(django_filters.FilterSet):
    """
    Фильтры для эндпоинта списка психологов.

    Query-параметры:
        specialization: Slug специализации (совпадение через M2M-таблицу связи).
        min_price: Минимальная цена сессии (включительно).
        max_price: Максимальная цена сессии (включительно).
        is_verified: Статус верификации (в основном для админа).
    """

    specialization = django_filters.CharFilter(
        field_name='specializations__slug',
        lookup_expr='exact',
        label='Specialization slug',
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Minimum price',
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Maximum price',
    )
    is_verified = django_filters.BooleanFilter(
        field_name='is_verified',
        label='Verified',
    )

    class Meta:
        model = PsychologistProfile
        fields = ['specialization', 'min_price', 'max_price', 'is_verified']
