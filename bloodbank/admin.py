from django.contrib import admin
from .models import BloodInventory, BloodRequest


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'location_name', 'city', 'units_available', 'last_updated')
    list_filter = ('blood_group', 'city')
    search_fields = ('blood_group', 'location_name', 'city')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('requester_name', 'phone', 'blood_group', 'city', 'urgency', 'created_at')
    list_filter = ('urgency', 'city')
    search_fields = ('requester_name', 'phone', 'blood_group', 'city')