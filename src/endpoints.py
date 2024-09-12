from flask import Blueprint, request, jsonify
from http import HTTPStatus
from datetime import datetime, timedelta, time, timezone
from src.extensions import db
from src.models import Doctor, Appointment
from src.schemas import AppointmentSchema, TimeWindowSchema, AvailableAppointmentSchema
from marshmallow import ValidationError

schedule = Blueprint('schedule', __name__)


# Initialize the database
def init_db():
    if Doctor.query.count() == 0:
        strange = Doctor(name='Strange', work_start=time(9, 0), work_end=time(17, 0), days=[1, 2, 3, 4, 5])
        who = Doctor(name='Who', work_start=time(8, 0), work_end=time(16, 0), days=[1, 2, 3, 4, 5])
        db.session.add_all([strange, who])
        db.session.commit()

@schedule.route('/init_db', methods=['POST'])
def initialize_db():
    if Doctor.query.count() > 0:
        return jsonify({"message": "Init already done."}), HTTPStatus.BAD_REQUEST
    init_db()
    return jsonify({"message": "Database initialized with doctors."}), HTTPStatus.OK


# Create an appointment
@schedule.route('/appointments', methods=['POST'])
def create_appointment():
    try:
        data = AppointmentSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    doctor = Doctor.query.get(data['doctor_id'])
    if not doctor:
        return jsonify({"message": "Doctor not found."}), HTTPStatus.NOT_FOUND

    start_time = data['start_time']
    duration = data['duration']
    end_time = start_time + timedelta(minutes=duration)

    if not doctor.is_working(start_time):
        return jsonify({"message": "Doctor not available at the specified time."}), HTTPStatus.BAD_REQUEST

    # Check for conflicts
    conflicting_appointments = Appointment.query.filter_by(doctor_id=doctor.id).filter(
        (Appointment.start_time < end_time) & (Appointment.end_time > start_time)).all()

    if conflicting_appointments:
        return jsonify({"message": "The time slot is already booked."}), HTTPStatus.CONFLICT

    appointment = Appointment(doctor_id=doctor.id, start_time=start_time, end_time=end_time)
    db.session.add(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment created successfully."}), HTTPStatus.CREATED


# Get appointments for a doctor within a time window
@schedule.route('/appointments', methods=['GET'])
def get_appointments():
    try:
        data = TimeWindowSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST
    
    doctor = Doctor.query.get(data['doctor_id'])
    if not doctor:
        return jsonify({"message": "Doctor not found."}), HTTPStatus.NOT_FOUND

    appointments = Appointment.query.filter_by(doctor_id=data['doctor_id']).filter(
        Appointment.start_time >= data['start_time'],
        Appointment.end_time <= data['end_time']
    ).all()

    return jsonify([{
        'id': appointment.id,
        'doctor_id': appointment.doctor_id,
        'start_time': appointment.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'end_time': appointment.end_time.strftime("%Y-%m-%dT%H:%M:%S")
    } for appointment in appointments]), HTTPStatus.OK


# Get the first available appointment after a specified time
@schedule.route('/appointments/available', methods=['GET'])
def get_available_appointment():
    try:
        data = AvailableAppointmentSchema().load(request.args)
    except ValidationError as err:
        return jsonify(err.messages), HTTPStatus.BAD_REQUEST

    after_time = data.get('after_time', datetime.now(timezone.utc))  # Default to current time if not provided
    doctor_id = data.get('doctor_id')

    doctors = [Doctor.query.get(doctor_id)] if doctor_id else Doctor.query.all()

    for doctor in doctors:
        current_time = after_time
        while current_time.time() < doctor.work_end:
            if doctor.is_working(current_time):
                conflicting_appointments = Appointment.query.filter_by(doctor_id=doctor.id).filter(
                    (Appointment.start_time < current_time + timedelta(minutes=15)) &
                    (Appointment.end_time > current_time)).all()

                if not conflicting_appointments:
                    return jsonify({
                        'doctor_id': doctor.id,
                        'doctor_name': doctor.name,
                        'start_time': current_time.strftime("%Y-%m-%dT%H:%M:%S"),
                        'end_time': (current_time + timedelta(minutes=15)).strftime("%Y-%m-%dT%H:%M:%S")
                    }), HTTPStatus.OK
            current_time += timedelta(minutes=15)

    return jsonify({"message": "No available slots."}), HTTPStatus.NOT_FOUND
