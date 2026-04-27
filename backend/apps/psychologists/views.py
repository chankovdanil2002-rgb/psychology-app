"""
Представления для публичного каталога психологов и административных эндпоинтов.
"""
from django.core.cache import cache
from django.db.models import Avg, Count, F, Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.psychologists.filters import PsychologistFilter
from apps.psychologists.models import PsychologistProfile
from apps.psychologists.serializers import (
    AdminPsychologistCreateSerializer,
    AdminPsychologistListSerializer,
    PsychologistDetailSerializer,
    PsychologistListSerializer,
)
from apps.users.permissions import IsAdmin
from apps.users.utils import success_response


@method_decorator(cache_page(300), name='dispatch')
class PsychologistListView(generics.ListAPIView):
    """
    Публичный каталог психологов.

    Показываются только верифицированные психологи с заполненным профилем.
    Поддерживает фильтрацию по slug специализации, диапазону цены, поиск по имени
    и сортировку по цене или среднему рейтингу.

    GET /api/psychologists/
    """

    serializer_class = PsychologistListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PsychologistFilter
    search_fields = ['first_name', 'last_name', 'patronymic', 'bio']
    ordering_fields = ['price', 'average_rating', 'experience_years']
    ordering = ['-average_rating']

    def get_queryset(self):
        """
        Возвращает только верифицированных психологов с заполненным профилем,
        с аннотациями average_rating и total_reviews.
        """
        return (
            PsychologistProfile.objects
            .filter(is_verified=True, is_profile_complete=True)
            .select_related('user')
            .prefetch_related('specializations')
            .annotate(
                average_rating=Avg(
                    'appointments__review__rating',
                    filter=Q(
                        appointments__status='completed',
                        appointments__review__isnull=False,
                    ),
                ),
                total_reviews=Count(
                    'appointments__review',
                    filter=Q(
                        appointments__status='completed',
                        appointments__review__isnull=False,
                    ),
                ),
            )
        )

    def filter_queryset(self, queryset):
        """
        После стандартной фильтрации заменяет сортировку по average_rating
        на NULLS LAST, чтобы психологи без отзывов опускались в конец списка.
        """
        queryset = super().filter_queryset(queryset)

        ordering = queryset.query.order_by
        if not ordering:
            return queryset

        new_ordering = []
        changed = False
        for term in ordering:
            if term == '-average_rating':
                new_ordering.append(F('average_rating').desc(nulls_last=True))
                changed = True
            elif term == 'average_rating':
                new_ordering.append(F('average_rating').asc(nulls_last=True))
                changed = True
            else:
                new_ordering.append(term)

        if changed:
            queryset = queryset.order_by(*new_ordering)

        return queryset

    def list(self, request, *args, **kwargs):
        """Оборачивает постраничный ответ в стандартный успешный формат."""
        response = super().list(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message='Список психологов получен.',
        )


@method_decorator(cache_page(600), name='dispatch')
class PsychologistDetailView(generics.RetrieveAPIView):
    """
    Публичная страница одного психолога.

    GET /api/psychologists/<id>/
    """

    serializer_class = PsychologistDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Возвращает только верифицированных психологов с заполненным профилем,
        с аннотациями average_rating и total_reviews.
        """
        return (
            PsychologistProfile.objects
            .filter(is_verified=True, is_profile_complete=True)
            .select_related('user')
            .prefetch_related('specializations')
            .annotate(
                average_rating=Avg(
                    'appointments__review__rating',
                    filter=Q(
                        appointments__status='completed',
                        appointments__review__isnull=False,
                    ),
                ),
                total_reviews=Count(
                    'appointments__review',
                    filter=Q(
                        appointments__status='completed',
                        appointments__review__isnull=False,
                    ),
                ),
            )
        )

    def retrieve(self, request, *args, **kwargs):
        """Оборачивает ответ в стандартный успешный формат."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            data=serializer.data,
            message='Данные психолога получены.',
        )


class AdminPsychologistDeleteView(generics.DestroyAPIView):
    """
    Административный эндпоинт для удаления психолога.

    DELETE /api/admin/psychologists/<id>/
    Удаляет пользователя и связанный профиль психолога.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        return PsychologistProfile.objects.filter(user__role='psychologist').select_related('user')

    def destroy(self, request, *args, **kwargs):
        from django.db import transaction
        from apps.appointments.models import Appointment
        from apps.schedule.models import TimeSlot

        profile = self.get_object()
        user = profile.user
        name = str(profile)

        with transaction.atomic():
            # 1. Удаляем записи психолога (вместе с отзывами через CASCADE).
            #    Это разблокирует тайм-слоты (PROTECT снимается).
            Appointment.objects.filter(psychologist=profile).delete()
            # 2. Удаляем тайм-слоты.
            TimeSlot.objects.filter(psychologist=profile).delete()
            # 3. Удаляем пользователя — каскадно удаляет профиль.
            user.delete()

        cache.clear()
        return success_response(
            message=f'Психолог «{name}» успешно удалён.',
            status_code=status.HTTP_200_OK,
        )


class AdminPsychologistListCreateView(generics.ListCreateAPIView):
    """
    Административный эндпоинт для управления командой психологов.

    GET /api/admin/psychologists/
    POST /api/admin/psychologists/
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        """Использует разные сериализаторы для list и create."""
        if self.request.method == 'POST':
            return AdminPsychologistCreateSerializer
        return AdminPsychologistListSerializer

    def get_queryset(self):
        """Возвращает всех психологов, отсортированных по дате создания."""
        return (
            PsychologistProfile.objects
            .filter(user__role='psychologist')
            .select_related('user')
            .order_by('-user__date_joined')
        )

    def list(self, request, *args, **kwargs):
        """Оборачивает ответ в стандартный успешный формат."""
        response = super().list(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message='Список психологов получен.',
        )

    def create(self, request, *args, **kwargs):
        """Создаёт аккаунт психолога и инвалидирует кэш страниц каталога."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        cache.clear()

        return success_response(
            data=AdminPsychologistListSerializer(profile).data,
            message='Аккаунт психолога успешно создан.',
            status_code=status.HTTP_201_CREATED,
        )
