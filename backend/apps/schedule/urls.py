"""URL configuration for the schedule app."""
from django.urls import path

from . import views

app_name = 'schedule'

urlpatterns = [
    path(
        'slots/',
        views.TimeSlotListView.as_view(),
        name='timeslot-list',
    ),
    path(
        'slots/create/',
        views.TimeSlotCreateView.as_view(),
        name='timeslot-create',
    ),
    path(
        'slots/bulk/',
        views.TimeSlotBulkCreateView.as_view(),
        name='timeslot-bulk-create',
    ),
    path(
        'slots/<int:pk>/',
        views.TimeSlotDeleteView.as_view(),
        name='timeslot-delete',
    ),
]
