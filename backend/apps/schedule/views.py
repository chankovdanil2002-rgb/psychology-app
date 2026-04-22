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

    Публичный эндпоинт. Возвращает доступные тайм-слоты с опциональной
    фильтрацией по id психолога и/или дате.
    """

    permission_classes = [AllowAny]
    serializer_class = TimeSlotSerializer

    def get_queryset(self):
        qs = TimeSlot.objects.select_related('psychologist').filter(
            is_available=True,
        )
        psychologist_id = self.request.query_params.get('psychologist')
        if psychologist_id:
            qs = qs.filter(psychologist_id=psychologist_id)

        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(date=date)

        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data,
            message='Time slots retrieved successfully.',
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
            message='Time slot created successfully.',
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
            message=f'{len(created_slots)} time slot(s) created successfully.',
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
        if hasattr(instance, 'appointment'):
            return success_response(
                data={},
                message='Cannot delete a time slot that has a linked appointment.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        instance.delete()
        return success_response(
            message='Time slot deleted successfully.',
            status_code=status.HTTP_200_OK,
        )
