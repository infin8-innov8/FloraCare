from django.db import models


class AmbulanceUnit(models.Model):
    unit_name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    IS_AVAILABLE_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
    ]
    is_available = models.CharField(max_length=10, choices=IS_AVAILABLE_CHOICES, default='available')

    class Meta:
        ordering = ['unit_name']

    def __str__(self):
        return self.unit_name


class AmbulanceRequest(models.Model):
    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Dispatched', 'Dispatched'),
        ('Completed', 'Completed'),
    ]

    patient_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    pickup_location = models.CharField(max_length=200)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-requested_at']

    def __str__(self):
        return f"Request for {self.patient_name} - {self.status}"