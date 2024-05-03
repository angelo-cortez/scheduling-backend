# Standard library imports
from datetime import datetime
import json

# Django imports
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

# Local application imports
from .models import Doctor, Appointment
from .helpers import parse_request_data, validate_date_time, get_doctor, check_appointment_limit

@csrf_exempt # This is a temporary solution to allow POST requests without CSRF token
@require_http_methods(["POST"])
def add_doctor(request):
    data = json.loads(request.body)

    # Validate the data
    required_fields = ['first_name', 'last_name']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return HttpResponseBadRequest(f'Missing or empty required fields: {", ".join(missing_fields)}')

    # Create a new doctor
    doctor = Doctor.objects.create(first_name=data['first_name'], last_name=data['last_name'])

    return JsonResponse({"id": doctor.id, "message": "Doctor added"})

@require_http_methods(["GET"])
def list_doctors(request):
    doctors = Doctor.objects.all().values()
    return JsonResponse(list(doctors), safe=False)


@require_http_methods(["GET"])
def list_appointments(request, doctor_id, date):
    date = parse_datetime(date)
    start_of_day = timezone.make_aware(datetime.combine(date, datetime.min.time()))
    end_of_day = timezone.make_aware(datetime.combine(date, datetime.max.time()))
    appointments = Appointment.objects.filter(doctor_id=doctor_id, date_time__range=(start_of_day, end_of_day)).values()
    return JsonResponse(list(appointments), safe=False)

from django.db.models import Q

@csrf_exempt # This is a temporary solution to allow POST requests without CSRF token
@require_http_methods(["POST"])
def add_appointment(request):
    data, date_time, doctor_id = parse_request_data(request)

    if not validate_date_time(date_time):
        return HttpResponseBadRequest('Appointments can only start at 15 minute intervals.')

    doctor = get_doctor(doctor_id)

    if not check_appointment_limit(doctor, date_time):
        return HttpResponseBadRequest('No more than 3 appointments can be added with the same time for a given doctor.')

    appointment = Appointment.objects.create(doctor=doctor, **data)

    return JsonResponse({"id": appointment.id, "message": "Appointment added"})

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_appointment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)

    appointment.delete()
    return JsonResponse({"message": "Appointment deleted"})