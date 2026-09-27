from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from .models import Patient
from .forms import PatientForm


class PatientListView(ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    paginate_by = 20

    def get_queryset(self):
        queryset = Patient.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(phone__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PatientDetailView(DetailView):
    model = Patient
    template_name = 'patients/detail.html'


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'
    success_url = '/patients/'

    def form_valid(self, form):
        response = super().form_valid(form)
        return response