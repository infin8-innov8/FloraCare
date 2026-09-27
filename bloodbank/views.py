from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import BloodInventory, BloodRequest
from .forms import BloodRequestForm, BloodInventoryForm


class BloodInventoryListView(ListView):
    model = BloodInventory
    template_name = 'bloodbank/inventory.html'
    context_object_name = 'inventories'
    paginate_by = 20

    def get_queryset(self):
        blood_group = self.request.GET.get('blood_group')
        city = self.request.GET.get('city')
        
        queryset = BloodInventory.objects.all()
        
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        return queryset.order_by('blood_group', 'city')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blood_group_filter'] = self.request.GET.get('blood_group', '')
        context['city_filter'] = self.request.GET.get('city', '')
        return context


class BloodRequestCreateView(CreateView):
    model = BloodRequest
    form_class = BloodRequestForm
    template_name = 'bloodbank/request_form.html'
    success_url = '/bloodbank/request/list/'


@login_required
def bloodbank_inventory(request):
    return BloodInventoryListView.as_view()(request)


@login_required
def blood_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blood_request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'bloodbank/request_form.html', {'form': form})


class BloodRequestListView(ListView):
    model = BloodRequest
    template_name = 'bloodbank/request_list.html'
    context_object_name = 'requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = BloodRequest.objects.all()
        urgency = self.request.GET.get('urgency')
        blood_group = self.request.GET.get('blood_group')
        city = self.request.GET.get('city')
        
        if urgency:
            queryset = queryset.filter(urgency=urgency)
        if blood_group:
            queryset = queryset.filter(blood_group=blood_group)
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        return queryset.order_by('-created_at')


class BloodRequestDetailView(DetailView):
    model = BloodRequest
    template_name = 'bloodbank/request_detail.html'