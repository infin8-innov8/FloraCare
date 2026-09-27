from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from patients.models import Patient
from appointments.models import Appointment
from ambulance.models import AmbulanceUnit, AmbulanceRequest
from bloodbank.models import BloodInventory, BloodRequest


@login_required
def dashboard(request):
    # Total patients
    total_patients = Patient.objects.count()

    # Appointment counts by status (single aggregated query)
    appointment_counts = Appointment.objects.values('status').annotate(count=Count('id'))

    # Ambulance available/busy counts
    ambulance_available = AmbulanceUnit.objects.filter(is_available='available').count()
    ambulance_busy = AmbulanceUnit.objects.filter(is_available='busy').count()

    # Total blood units available
    total_blood_units = BloodInventory.objects.aggregate(total=Count('units_available'))['total'] or 0

    # Prepare chart data
    # 1. Appointment status distribution - pie chart
    status_labels = []
    status_data = []
    for item in appointment_counts:
        status_labels.append(item['status'])
        status_data.append(item['count'])

    # 2. Blood inventory by group - bar chart
    blood_group_data = {}
    blood_inventory = BloodInventory.objects.all()
    for item in blood_inventory:
        if item.blood_group not in blood_group_data:
            blood_group_data[item.blood_group] = 0
        blood_group_data[item.blood_group] += item.units_available

    blood_group_labels = list(blood_group_data.keys())
    blood_group_values = list(blood_group_data.values())

    context = {
        'total_patients': total_patients,
        'appointment_counts': appointment_counts,
        'ambulance_available': ambulance_available,
        'ambulance_busy': ambulance_busy,
        'total_blood_units': total_blood_units,
        'status_labels': status_labels,
        'status_data': status_data,
        'blood_group_labels': blood_group_labels,
        'blood_group_values': blood_group_values,
    }
    return render(request, 'dashboard/index.html', context)