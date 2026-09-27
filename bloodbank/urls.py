from django.urls import path
from . import views

app_name = 'bloodbank'

urlpatterns = [
    path('inventory/', views.BloodInventoryListView.as_view(), name='bloodbank_inventory'),
    path('request/', views.BloodRequestCreateView.as_view(), name='blood_request'),
    path('request/list/', views.BloodRequestListView.as_view(), name='blood_request_list'),
    path('detail/<int:pk>/', views.BloodRequestDetailView.as_view(), name='blood_request_detail'),
]