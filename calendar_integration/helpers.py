# Standard library imports
from datetime import datetime
import json

# Django imports
from django.db.models import Q

# Local application imports
from .models import Doctor, Appointment


def parse_request_data(request):
    data = json.loads(request.body)
    date_time = data.get('date_time')
    date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ")
    doctor_id = data.pop('doctor')
    return data, date_time, doctor_id

def validate_date_time(date_time):
    if date_time.minute % 15 != 0:
        return False
    return True

def get_doctor(doctor_id):
    return Doctor.objects.get(id=doctor_id)

def check_appointment_limit(doctor, date_time):
    same_time_appointments = Appointment.objects.filter(
        Q(doctor=doctor) & 
        Q(date_time__year=date_time.year) & 
        Q(date_time__month=date_time.month) & 
        Q(date_time__day=date_time.day) & 
        Q(date_time__hour=date_time.hour) & 
        Q(date_time__minute=date_time.minute)
    )
    if same_time_appointments.count() >= 3:
        return False
    return True
