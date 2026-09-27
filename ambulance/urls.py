from django.urls import path
from . import views

app_name = 'ambulance'

urlpatterns = [
    path('request/', views.AmbulanceRequestCreateView.as_view(), name='ambulance_request'),
    path('available/', views.AmbulanceAvailableListView.as_view(), name='ambulance_available'),
    path('request/list/', views.AmbulanceRequestListView.as_view(), name='ambulance_request_list'),
    path('request/detail/<int:pk>/', views.AmbulanceRequestDetailView.as_view(), name='ambulance_request_detail'),
]