from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('register/', views.PatientCreateView.as_view(), name='patient_create'),
    path('', views.PatientListView.as_view(), name='patient_list'),
    path('search/', views.PatientListView.as_view(), name='patient_search'),
    path('detail/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
]