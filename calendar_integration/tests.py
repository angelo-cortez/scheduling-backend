# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Doctor, Appointment
from datetime import datetime, timedelta
import json

class AppointmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.doctor = Doctor.objects.create(first_name="Dr.", last_name="Test")
        self.appointment_data = {
            "doctor": self.doctor.id,
            "patient_first_name": "John",
            "patient_last_name": "Doe",
            "date_time": (datetime.now() + timedelta(days=1)).isoformat() + "Z",
            "kind": "New Patient"
        }

    def test_add_appointment_success(self):
        # Modify the date_time in appointment_data to have minute value as 15 and no fractional seconds
        self.appointment_data['date_time'] = datetime.now().replace(minute=15, microsecond=0).isoformat() + "Z"
        
        response = self.client.post(
            reverse('add_appointment'), 
            data=json.dumps(self.appointment_data), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_add_appointment_failure(self):
        # Modify the date_time in appointment_data to have minute value not equal to 15 and no fractional seconds
        self.appointment_data['date_time'] = datetime.now().replace(minute=16, microsecond=0).isoformat() + "Z"
        
        response = self.client.post(
            reverse('add_appointment'), 
            data=json.dumps(self.appointment_data), 
            content_type='application/json'
        )
        # Assuming your API returns a 400 status code for invalid minute value
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 0)
    def test_add_appointments_limit(self):
        # Add 3 appointments successfully
        for _ in range(3):
            self.appointment_data['date_time'] = datetime.now().replace(minute=15, microsecond=0).isoformat() + "Z"
            response = self.client.post(
                reverse('add_appointment'), 
                data=json.dumps(self.appointment_data), 
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
        self.assertEqual(Appointment.objects.count(), 3)

        # Try to add a 4th appointment and expect failure
        self.appointment_data['date_time'] = datetime.now().replace(minute=15, microsecond=0).isoformat() + "Z"
        response = self.client.post(
            reverse('add_appointment'), 
            data=json.dumps(self.appointment_data), 
            content_type='application/json'
        )
        # Assuming your API returns a 400 status code for exceeding the limit
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 3)