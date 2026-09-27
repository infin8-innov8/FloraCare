from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor_name', 'scheduled_time', 'status', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'scheduled_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }