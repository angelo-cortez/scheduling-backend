from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.list_doctors, name='list_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('appointments/<int:doctor_id>/<str:date>/', views.list_appointments, name='list_appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
]
