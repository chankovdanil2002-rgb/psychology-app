"""URL configuration for the reviews app."""
from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path(
        '',
        views.ReviewListView.as_view(),
        name='review-list',
    ),
    path(
        'create/',
        views.ReviewCreateView.as_view(),
        name='review-create',
    ),
]
