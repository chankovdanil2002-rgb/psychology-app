"""Представления для приложения appointments."""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.users.permissions import IsClient, IsProfileComplete, IsPsychologist
from apps.users.utils import success_response

from .models import Appointment
from .serializers import (
    AppointmentCreateSerializer,
    AppointmentDetailSerializer,
    AppointmentListSerializer,
)


class AppointmentCreateView(APIView):
    """
    POST /api/appointments/

    Создаёт новую запись на приём. Только для клиента с заполненным профилем.
    """

    permission_classes = [IsAuthenticated, IsClient, IsProfileComplete]

    def post(self, request):
        serializer = AppointmentCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        return success_response(
            data=AppointmentDetailSerializer(appointment).data,
            message='Appointment created successfully.',
            status_code=status.HTTP_201_CREATED,
        )


class AppointmentListView(APIView):
    """
    GET /api/appointments/

    Возвращает записи текущего пользователя в зависимости от его роли.
    Клиенты видят свои записи; психологи — входящие заявки.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == 'client':
            qs = Appointment.objects.filter(
                client=user.client_profile,
            )
        elif user.role == 'psychologist':
            qs = Appointment.objects.filter(
                psychologist=user.psychologist_profile,
            )
        else:
            qs = Appointment.objects.none()

        qs = qs.select_related(
            'client', 'psychologist', 'time_slot',
        ).order_by('-created_at')

        serializer = AppointmentListSerializer(qs, many=True)
        return success_response(
            data=serializer.data,
            message='Appointments retrieved successfully.',
        )


class AppointmentConfirmView(APIView):
    """
    PATCH /api/appointments/<id>/confirm/

    Психолог подтверждает запись со статусом pending.
    """

    permission_classes = [IsAuthenticated, IsPsychologist]

    def patch(self, request, pk):
        appointment = self._get_appointment(pk, request.user)
        if appointment is None:
            return success_response(
                data={},
                message='Appointment not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status != Appointment.Status.PENDING:
            return success_response(
                data={},
                message='Only pending appointments can be confirmed.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = Appointment.Status.CONFIRMED
        appointment.save(update_fields=['status', 'updated_at'])
        return success_response(
            data=AppointmentDetailSerializer(appointment).data,
            message='Appointment confirmed.',
        )

    @staticmethod
    def _get_appointment(pk, user):
        try:
            return Appointment.objects.select_related(
                'client', 'psychologist', 'time_slot',
            ).get(pk=pk, psychologist=user.psychologist_profile)
        except Appointment.DoesNotExist:
            return None


class AppointmentRejectView(APIView):
    """
    PATCH /api/appointments/<id>/reject/

    Психолог отклоняет запись со статусом pending. Освобождает тайм-слот.
    """

    permission_classes = [IsAuthenticated, IsPsychologist]

    def patch(self, request, pk):
        appointment = self._get_appointment(pk, request.user)
        if appointment is None:
            return success_response(
                data={},
                message='Appointment not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status != Appointment.Status.PENDING:
            return success_response(
                data={},
                message='Only pending appointments can be rejected.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = Appointment.Status.REJECTED
        appointment.save(update_fields=['status', 'updated_at'])

        # Освобождаем слот.
        slot = appointment.time_slot
        slot.is_available = True
        slot.save(update_fields=['is_available'])

        return success_response(
            data=AppointmentDetailSerializer(appointment).data,
            message='Appointment rejected. Time slot released.',
        )

    @staticmethod
    def _get_appointment(pk, user):
        try:
            return Appointment.objects.select_related(
                'client', 'psychologist', 'time_slot',
            ).get(pk=pk, psychologist=user.psychologist_profile)
        except Appointment.DoesNotExist:
            return None


class AppointmentCompleteView(APIView):
    """
    PATCH /api/appointments/<id>/complete/

    Психолог отмечает подтверждённую запись как завершённую.
    """

    permission_classes = [IsAuthenticated, IsPsychologist]

    def patch(self, request, pk):
        appointment = self._get_appointment(pk, request.user)
        if appointment is None:
            return success_response(
                data={},
                message='Appointment not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status != Appointment.Status.CONFIRMED:
            return success_response(
                data={},
                message='Only confirmed appointments can be completed.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = Appointment.Status.COMPLETED
        appointment.save(update_fields=['status', 'updated_at'])
        return success_response(
            data=AppointmentDetailSerializer(appointment).data,
            message='Appointment marked as completed.',
        )

    @staticmethod
    def _get_appointment(pk, user):
        try:
            return Appointment.objects.select_related(
                'client', 'psychologist', 'time_slot',
            ).get(pk=pk, psychologist=user.psychologist_profile)
        except Appointment.DoesNotExist:
            return None


class AppointmentCancelView(APIView):
    """
    PATCH /api/appointments/<id>/cancel/

    Клиент отменяет запись со статусом pending или confirmed. Освобождает
    тайм-слот.
    """

    permission_classes = [IsAuthenticated, IsClient]

    def patch(self, request, pk):
        try:
            appointment = Appointment.objects.select_related(
                'client', 'psychologist', 'time_slot',
            ).get(pk=pk, client=request.user.client_profile)
        except Appointment.DoesNotExist:
            return success_response(
                data={},
                message='Appointment not found.',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        if appointment.status not in (
            Appointment.Status.PENDING,
            Appointment.Status.CONFIRMED,
        ):
            return success_response(
                data={},
                message='Only pending or confirmed appointments can be cancelled.',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=['status', 'updated_at'])

        # Освобождаем слот.
        slot = appointment.time_slot
        slot.is_available = True
        slot.save(update_fields=['is_available'])

        return success_response(
            data=AppointmentDetailSerializer(appointment).data,
            message='Appointment cancelled. Time slot released.',
        )
