from django.contrib import admin
from .models import AmbulanceUnit, AmbulanceRequest


@admin.register(AmbulanceUnit)
class AmbulanceUnitAdmin(admin.ModelAdmin):
    list_display = ('unit_name', 'current_location', 'latitude', 'longitude', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('unit_name', 'current_location')


@admin.register(AmbulanceRequest)
class AmbulanceRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'phone', 'pickup_location', 'status', 'requested_at')
    list_filter = ('status',)
    search_fields = ('patient_name', 'phone')