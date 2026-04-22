"""Admin configuration for the specializations app."""
from django.contrib import admin

from .models import PsychologistSpecialization, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    """Admin view for Specialization."""

    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PsychologistSpecialization)
class PsychologistSpecializationAdmin(admin.ModelAdmin):
    """Admin view for PsychologistSpecialization."""

    list_display = ('psychologist', 'specialization', 'is_primary')
    list_filter = ('is_primary', 'specialization')
    raw_id_fields = ('psychologist',)
