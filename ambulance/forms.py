from django import forms
from .models import AmbulanceUnit, AmbulanceRequest


class AmbulanceRequestForm(forms.ModelForm):
    class Meta:
        model = AmbulanceRequest
        fields = ['patient_name', 'phone', 'pickup_location', 'pickup_latitude', 'pickup_longitude', 'status']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_location': forms.TextInput(attrs={'class': 'form-control'}),
            'pickup_latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'pickup_longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class AmbulanceUnitForm(forms.ModelForm):
    class Meta:
        model = AmbulanceUnit
        fields = ['unit_name', 'current_location', 'latitude', 'longitude', 'is_available']
        widgets = {
            'unit_name': forms.TextInput(attrs={'class': 'form-control'}),
            'current_location': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.Select(attrs={'class': 'form-control'}),
        }