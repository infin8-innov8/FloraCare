from django.db import models


class BloodInventory(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    location_name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    units_available = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['blood_group', 'city']

    def __str__(self):
        return f"{self.blood_group} - {self.location_name} ({self.city})"


class BloodRequest(models.Model):
    REQUESTER_NAME_CHOICES = [
        ('requester', 'Requester'),
    ]
    URGENCY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    requester_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=3)
    city = models.CharField(max_length=100)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.requester_name} - {self.blood_group} - {self.city} - {self.urgency}"