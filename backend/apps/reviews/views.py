"""Представления для приложения reviews."""
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from apps.users.permissions import IsClient
from apps.users.utils import success_response

from .models import Review
from .serializers import ReviewCreateSerializer, ReviewSerializer


class ReviewCreateView(APIView):
    """
    POST /api/reviews/

    Создаёт отзыв к завершённой записи. Только для клиента.
    """

    permission_classes = [IsAuthenticated, IsClient]

    def post(self, request):
        serializer = ReviewCreateSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        return success_response(
            data=ReviewSerializer(review).data,
            message='Отзыв успешно оставлен.',
            status_code=status.HTTP_201_CREATED,
        )


class ReviewListView(APIView):
    """
    GET /api/reviews/?psychologist=<id>

    Возвращает отзывы с опциональной фильтрацией по id психолога.
    Публичный эндпоинт.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        qs = Review.objects.select_related(
            'appointment__client',
            'appointment__psychologist',
            'appointment__time_slot',
        ).order_by('-created_at')

        psychologist_id = request.query_params.get('psychologist')
        if psychologist_id:
            qs = qs.filter(appointment__psychologist_id=psychologist_id)

        serializer = ReviewSerializer(qs, many=True)
        return success_response(
            data=serializer.data,
            message='Список отзывов получен.',
        )
