from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'phone', 'blood_group', 'created_at')
    search_fields = ('name', 'phone', 'blood_group')
    list_filter = ('gender', 'blood_group', 'created_at')