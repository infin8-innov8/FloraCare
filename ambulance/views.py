import math
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from .models import AmbulanceUnit, AmbulanceRequest
from .forms import AmbulanceRequestForm, AmbulanceUnitForm


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in kilometers
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


class AmbulanceRequestCreateView(CreateView):
    model = AmbulanceRequest
    form_class = AmbulanceRequestForm
    template_name = 'ambulance/request_form.html'
    success_url = '/ambulance/request/list/'

    def form_valid(self, form):
        form.instance.requested_at = timezone.now()
        return super().form_valid(form)


class AmbulanceAvailableListView(ListView):
    model = AmbulanceUnit
    template_name = 'ambulance/available.html'
    context_object_name = 'units'

    def get_queryset(self):
        pickup_lat = float(self.request.GET.get('pickup_lat', 0))
        pickup_lon = float(self.request.GET.get('pickup_lon', 0))
        
        queryset = AmbulanceUnit.objects.filter(is_available='available')
        
        # Calculate distance for each unit and sort
        distances = []
        for unit in queryset:
            dist = haversine(pickup_lat, pickup_lon, unit.latitude, unit.longitude)
            distances.append((unit, dist))
        
        # Sort by distance (closest first)
        distances.sort(key=lambda x: x[1])
        
        # Return sorted units
        self.units_with_distance = distances
        return [unit for unit, dist in distances]


class AmbulanceRequestListView(ListView):
    model = AmbulanceRequest
    template_name = 'ambulance/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = AmbulanceRequest.objects.all()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-requested_at')


class AmbulanceRequestDetailView(DetailView):
    model = AmbulanceRequest
    template_name = 'ambulance/request_detail.html'