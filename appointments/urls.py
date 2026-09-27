from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.AppointmentBookView.as_view(), name='appointment_book'),
    path('upcoming/', views.AppointmentUpcomingView.as_view(), name='appointment_upcoming'),
    path('detail/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('update-status/<int:pk>/', views.AppointmentUpdateStatusView.as_view(), name='appointment_update_status'),
]