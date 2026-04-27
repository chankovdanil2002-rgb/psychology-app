"""URL-конфигурация приложения appointments."""
from django.urls import path

from . import views

app_name = 'appointments'

urlpatterns = [
    path(
        '',
        views.AppointmentListView.as_view(),
        name='appointment-list',
    ),
    path(
        'create/',
        views.AppointmentCreateView.as_view(),
        name='appointment-create',
    ),
    path(
        '<int:pk>/confirm/',
        views.AppointmentConfirmView.as_view(),
        name='appointment-confirm',
    ),
    path(
        '<int:pk>/reject/',
        views.AppointmentRejectView.as_view(),
        name='appointment-reject',
    ),
    path(
        '<int:pk>/complete/',
        views.AppointmentCompleteView.as_view(),
        name='appointment-complete',
    ),
    path(
        '<int:pk>/cancel/',
        views.AppointmentCancelView.as_view(),
        name='appointment-cancel',
    ),
]
