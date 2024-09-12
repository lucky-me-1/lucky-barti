import pytest
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from src.extensions import db

two_pm = datetime.now(timezone.utc).replace(hour=14, minute=0, second=0, microsecond=0)

def get_date_for_day(dayIndex):
    today = datetime.today()
    today_index = today.weekday() + 1  # 0 is Monday, so we adjust it to make Sunday 0
    days_ahead = (dayIndex - today_index) % 7  # Calculate how many days ahead
    if days_ahead == 0:
        days_ahead = 7  # If the day is today, return the same day next week
    return today + timedelta(days=days_ahead)

def test_init_db(client):
    response = client.post('/init_db')
    assert response.status_code == HTTPStatus.OK

    response = client.post('/init_db')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json['message'] == "Init already done."

def test_get_appointments_within_window_no_doctor(client):
    start_time = (datetime.now() + timedelta(days=1))
    end_time = (start_time + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S")
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Get appointments within a time window
    response = client.get(f"/appointments?doctor_id=-1&start_time={start_time}&end_time={end_time}")
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json["message"] == 'Doctor not found.'
    

def test_create_appointment(client):
    client.post('/init_db')

    response = client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': two_pm.isoformat(),
        'duration': 45
    })
    assert response.status_code == HTTPStatus.CREATED
    
def test_create_appointment_bad_doctorid(client):
    client.post('/init_db')

    response = client.post('/appointments', json={
        'doctor_id': -1,
        'start_time': two_pm.isoformat(),
        'duration': 45
    })
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json["message"] == 'Doctor not found.'
    

def test_create_appointment_doc_not_working(client):
    client.post('/init_db')
    
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': (datetime.now() + timedelta(days=1)).replace(hour=0).strftime("%Y-%m-%dT%H:%M:%S"),
        'duration': 45
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["message"] == 'Doctor not available at the specified time.'
    
    
def test_create_appointment_bad_request(client):

    # Create an appointment for Doctor Strange
    response = client.post('/appointments', json={
        'start_time': 'lucky is kewl',
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    
def test_create_conflicting_appointment(client):
    client.post('/init_db')

    start_time = two_pm

    # Create the first appointment
    client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': start_time.isoformat(),
        'duration': 45
    })

    # Attempt to create a conflicting appointment
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': (start_time + timedelta(minutes=20)).isoformat(),
        'duration': 45
    })
    assert response.status_code == HTTPStatus.CONFLICT


def test_get_appointments_within_window(client):
    client.post('/init_db')
    
    response = client.get('/appointments/available?doctor_id=1&after_time=' + 
        (datetime.now() + timedelta(days=1)).replace(hour=14, microsecond=0).isoformat())
    
    start_time = datetime.fromisoformat(response.json['start_time'])
    start_time = (start_time + timedelta(minutes=15)).replace(microsecond=0)
    orig_time = start_time

    # Create an appointment for Doctor Strange
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': start_time.isoformat(),
        'duration': 45
    })
    assert response.status_code == HTTPStatus.CREATED
    
    start_time = (start_time - timedelta(hours=2))
    end_time = (start_time + timedelta(hours=4))
    
    # Get appointments within a time window
    response = client.get(f"/appointments?doctor_id=1&start_time={start_time.isoformat()}&end_time={end_time.isoformat()}")
    start_time = datetime.fromisoformat(response.json[0]['start_time'])
    
    assert response.status_code == HTTPStatus.OK
    assert orig_time == start_time

    
    
def test_get_appointments_within_window_bad_request(client):
    response = client.get(f"/appointments?doctor_id=1")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    

def test_get_first_available_appointment_no_after_time(client):
    client.post('/init_db')

    # Get the first available appointment without after_time
    response = client.get('/appointments/available')
    assert response.status_code == HTTPStatus.OK
    assert datetime.fromisoformat(response.json['start_time']) > (datetime.now() - timedelta(minutes=15))
    
def test_get_first_available_appointment_bad_request(client):
    client.post('/init_db')

    # Get the first available appointment without after_time
    response = client.get('/appointments/available?doctor_id=ABC')
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_first_available_appointment_with_after_time(client):
    client.post('/init_db')

    next_tuesday_9am = get_date_for_day(2).replace(hour=9, minute=0, second=0, microsecond=0)

    response = client.get('/appointments/available?after_time=' + next_tuesday_9am.strftime("%Y-%m-%dT%H:%M:%S"))
    assert response.status_code == HTTPStatus.OK
    assert next_tuesday_9am == datetime.fromisoformat(response.json['start_time'])


def test_get_first_available_appointment_no_available(client):
    client.post('/init_db')

    next_sunday_12am = get_date_for_day(0).replace(hour=0, minute=0, second=0, microsecond=0)

    response = client.get('/appointments/available?after_time=' + next_sunday_12am.strftime("%Y-%m-%dT%H:%M:%S"))
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json["message"] == 'No available slots.'
    
    
def test_create_appointment_invalid_start(client):
    client.post('/init_db')
    s = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    response = client.post('/appointments', json={
        'doctor_id': 1,
        'start_time': s,
        'duration': 45
    })
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["start_time"] == ['Start time must be in the future.']


def test_get_appointments_invalid_start_and_end(client):
    start_time = (datetime.now() + timedelta(days=2))
    end_time = (start_time - timedelta(hours=1))
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Get appointments within a time window
    response = client.get(f"/appointments?doctor_id=-1&start_time={start_time}&end_time={end_time}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json["_schema"] == ['Start time must be earlier than end time.']