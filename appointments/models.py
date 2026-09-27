from django.db import models
from patients.models import Patient


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-show', 'No-show'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=200)
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=0)

    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f"{self.patient.name} - {self.doctor_name} - {self.status}"