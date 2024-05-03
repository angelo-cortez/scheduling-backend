Project Endpoints Guide

1. Open Terminal.

2. Navigate to your project directory:

```bash
cd /path/to/your/project
```

3. Create a new virtual environment inside your project directory, activate it, and install your requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4.   Now you can run your tests:

```bash
python manage.py test
```



Alternatively, you can use your command line to test manually:

Base URL
All endpoints are located under the `api/` path. The base URL for all endpoints is `http://127.0.0.1:8000/api/`

## Endpoints

### Doctors

- **Endpoint:** `doctors/`
- **Method:** GET
- **Description:** Returns a list of all doctors.
- **Example command:** 

```bash
curl http://127.0.0.1:8000/api/doctors/
```


### Appointments

- **Endpoint:** `appointments/<int:doctor_id>/<str:date>/`
- **Method:** GET
- **Description:** Returns a list of all appointments for a specific doctor on a specific date.
- **Parameters:**
  - `doctor_id`: The ID of the doctor.
  - `date`: The date of the appointments in `YYYY-MM-DD` format.
- **Example command :** 
```bash
curl http://127.0.0.1:8000/api/appointments/1/2022-12-31/
```

### Add Appointment

- **Endpoint:** `appointments/add/`
- **Method:** POST
- **Description:** Adds a new appointment.
- **Example API URL:** 
```
curl -X POST -H "Content-Type: application/json" -d '{
    "doctor": 1,
    "patient_first_name": "John",
    "patient_last_name": "Doe",
    "date_time": "2022-12-31T15:30:00Z",
    "kind": "New Patient"
}' http://127.0.0.1:8000/api/appointments/add/
```

### Delete Appointment

- **Endpoint:** `appointments/delete/<int:appointment_id>/`
- **Method:** DELETE
- **Description:** Deletes a specific appointment.
- **Parameters:**
  - `appointment_id`: The ID of the appointment to delete.
- **Example URL:**

```bash
curl -X DELETE http://127.0.0.1:8000/api/appointments/delete/8/
```

Remember to start your Django server with `python manage.py runserver` before you try to access these URLs.