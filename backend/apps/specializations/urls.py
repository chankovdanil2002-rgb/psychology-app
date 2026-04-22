"""URL configuration for the specializations app."""
from django.urls import path

from . import views

app_name = 'specializations'

urlpatterns = [
    path('', views.SpecializationListView.as_view(), name='specialization-list'),
    path('<slug:slug>/', views.SpecializationDetailView.as_view(), name='specialization-detail'),
]
