from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q, Count, F
from django.db import transaction
from .models import Appointment
from patients.models import Patient
from .forms import AppointmentForm


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Appointment.objects.select_related('patient')
        query = self.request.GET.get('q')
        status = self.request.GET.get('status')
        doctor = self.request.GET.get('doctor')
        
        if query:
            queryset = queryset.filter(
                Q(patient__name__icontains=query) | Q(doctor_name__icontains=query)
            )
        if status:
            queryset = queryset.filter(status=status)
        if doctor:
            queryset = queryset.filter(doctor_name__icontains=doctor)
        
        return queryset.order_by('-scheduled_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['doctor_filter'] = self.request.GET.get('doctor', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'appointments/detail.html'


class AppointmentBookView(CreateView):
    form_class = AppointmentForm
    template_name = 'appointments/form.html'
    success_url = '/appointments/upcoming/'

    def form_valid(self, form):
        form.instance.version = 0
        return super().form_valid(form)


class AppointmentUpdateStatusView(DetailView):
    model = Appointment
    template_name = 'appointments/form.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        submitted_version = int(request.POST.get('version', 0))
        new_status = request.POST.get('status')
        new_notes = request.POST.get('notes', '')
        
        # Optimistic Concurrency Control
        updated = Appointment.objects.filter(
            pk=self.object.pk, version=submitted_version
        ).update(
            status=new_status,
            notes=new_notes,
            version=F('version') + 1
        )
        
        if not updated:
            return render(request, 'appointments/form.html', {
                'title': 'Update Appointment Status',
                'appointment': self.object,
                'error': 'This appointment was modified by another staff member. Please refresh and try again.',
            })
        
        return redirect('appointment_upcoming')
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return render(request, 'appointments/form.html', {
            'title': 'Update Appointment Status',
            'appointment': self.object,
        })


class AppointmentUpcomingView(ListView):
    model = Appointment
    template_name = 'appointments/upcoming.html'
    context_object_name = 'appointments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Appointment.objects.select_related('patient')
        date_filter = self.request.GET.get('date')
        status_filter = self.request.GET.get('status')
        doctor_filter = self.request.GET.get('doctor')
        
        if date_filter:
            queryset = queryset.filter(scheduled_time__date=date_filter)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if doctor_filter:
            queryset = queryset.filter(doctor_name__icontains=doctor_filter)
        
        return queryset.order_by('-scheduled_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_filter = self.request.GET.get('date', '')
        status_filter = self.request.GET.get('status', '')
        doctor_filter = self.request.GET.get('doctor', '')
        
        # Dashboard metrics: today's counts by status
        metrics_queryset = Appointment.objects.filter(
            scheduled_time__date=date_filter if date_filter else True
        ).values('status').annotate(count=Count('id'))
        
        metrics_dict = {item['status']: item['count'] for item in metrics_queryset}
        
        context['date_filter'] = date_filter
        context['status_filter'] = status_filter
        context['doctor_filter'] = doctor_filter
        context['metrics'] = metrics_dict
        return context