from django.db import models
from enum import Enum

class AppointmentType(Enum):
    NEW_PATIENT = 'New Patient'
    FOLLOW_UP = 'Follow-up'

class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_first_name = models.CharField(max_length=30)
    patient_last_name = models.CharField(max_length=30)
    date_time = models.DateTimeField()
    kind = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in AppointmentType]
    )
    def __str__(self):
        return f"{self.patient_first_name} {self.patient_last_name} - {self.date_time} ({self.kind})"
