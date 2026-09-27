from django.apps import AppConfig


class PatientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'patients'


class AmbulanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ambulance'


class BloodbankConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloodbank'


class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'