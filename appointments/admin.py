from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor_name', 'scheduled_time', 'status', 'version')
    search_fields = ('patient__name', 'doctor_name', 'status')
    list_filter = ('status', 'scheduled_time')