"""Представления для приложения schedule."""
from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.users.permissions import IsPsychologist, IsVerifiedPsychologist
from apps.users.utils import success_response

from .models import TimeSlot
from .serializers import (
    BulkTimeSlotCreateSerializer,
    TimeSlotCreateSerializer,
    TimeSlotSerializer,
)


class TimeSlotListView(ListAPIView):
    """
    GET /api/schedule/slots/?psychologist=<id>&date=<YYYY-MM-DD>

    Публичный эндпоинт. Возвращает доступные тайм-слоты.
    Параметр all=1 доступен только самому психологу — возвращает все слоты
    (включая занятые) для отображения расписания в личном кабинете.
    """

    permission_classes = [AllowAny]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        params = self.request.query_params
        psychologist_id = params.get('psychologist')
        date = params.get('date')
        show_all = params.get('all') == '1'

        # Психолог смотрит своё расписание — показываем все слоты
        user = self.request.user
        is_own_schedule = (
            show_all
            and user.is_authenticated
            and user.role == 'psychologist'
            and hasattr(user, 'psychologist_profile')
            and str(user.psychologist_profile.id) == str(psychologist_id)
        )

        if is_own_schedule:
            qs = TimeSlot.objects.select_related('psychologist').filter(
                psychologist_id=psychologist_id,
            )
        else:
            qs = TimeSlot.objects.select_related('psychologist').filter(
                is_available=True,
            )
            if psychologist_id:
                qs = qs.filter(psychologist_id=psychologist_id)

        if date:
            qs = qs.filter(date=date)

        return qs.order_by('date', 'start_time')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Список слотов получен.',
        )


class TimeSlotCreateView(APIView):
    """
    POST /api/schedule/slots/

    Создаёт один тайм-слот. Только для психолога.
    """

    permission_classes = [IsAuthenticated, IsPsychologist, IsVerifiedPsychologist]

    def post(self, request):
        serializer = TimeSlotCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        slot = serializer.save()
        return success_response(
            data=TimeSlotSerializer(slot).data,
            message='Слот успешно создан.',
            status_code=status.HTTP_201_CREATED,
        )


class TimeSlotBulkCreateView(APIView):
    """
    POST /api/schedule/slots/bulk/

    Массовое создание тайм-слотов в диапазоне дат. Только для психолога.
    """

    permission_classes = [IsAuthenticated, IsPsychologist, IsVerifiedPsychologist]

    def post(self, request):
        serializer = BulkTimeSlotCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        created_slots = serializer.save()
        return success_response(
            data=TimeSlotSerializer(created_slots, many=True).data,
            message=f'Создано слотов: {len(created_slots)}.',
            status_code=status.HTTP_201_CREATED,
        )


class TimeSlotDeleteView(DestroyAPIView):
    """
    DELETE /api/schedule/slots/<id>/

    Удаляет тайм-слот. Только для психолога-владельца слота.
    Нельзя удалить слот, привязанный к записи на приём.
    """

    permission_classes = [IsAuthenticated, IsPsychologist, IsVerifiedPsychologist]

    def get_queryset(self):
        return TimeSlot.objects.filter(
            psychologist=self.request.user.psychologist_profile,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Запрещаем удаление, если к слоту привязана запись.
        if instance.appointments.filter(status__in=['pending', 'confirmed']).exists():
            return success_response(
                data={},
                message='Нельзя удалить слот с активной записью.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        instance.delete()
        return success_response(
            message='Слот успешно удалён.',
            status_code=status.HTTP_200_OK,
        )
