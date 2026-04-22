"""Представления для приложения specializations."""
from django.db.models import Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from apps.users.utils import success_response

from .models import Specialization
from .serializers import SpecializationSerializer


@method_decorator(cache_page(1800), name='dispatch')
class SpecializationListView(ListAPIView):
    """
    GET /api/specializations/

    Возвращает список всех специализаций с количеством верифицированных
    психологов по каждой из них. Публичный эндпоинт.
    """

    permission_classes = [AllowAny]
    serializer_class = SpecializationSerializer

    def get_queryset(self):
        return Specialization.objects.annotate(
            psychologist_count=Count(
                'psychologist_specializations',
                filter=Q(
                    psychologist_specializations__psychologist__is_verified=True,
                    psychologist_specializations__psychologist__is_profile_complete=True,
                ),
            ),
        ).order_by('name')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Specializations retrieved successfully.',
        )


class SpecializationDetailView(RetrieveAPIView):
    """
    GET /api/specializations/<slug>/

    Возвращает детали одной специализации по slug. Публичный эндпоинт.
    """

    permission_classes = [AllowAny]
    serializer_class = SpecializationSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Specialization.objects.annotate(
            psychologist_count=Count(
                'psychologist_specializations',
                filter=Q(
                    psychologist_specializations__psychologist__is_verified=True,
                    psychologist_specializations__psychologist__is_profile_complete=True,
                ),
            ),
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='Specialization retrieved successfully.',
        )
