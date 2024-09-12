from marshmallow import Schema, fields, validates, validates_schema, ValidationError
import datetime

class AppointmentSchema(Schema):
    doctor_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    duration = fields.Int(required=True)  # Duration in minutes

    @validates('start_time')
    def validate_start_time(self, value):
        timezone = value.tzinfo
        if value < datetime.datetime.now(timezone):
            raise ValidationError('Start time must be in the future.')


class TimeWindowSchema(Schema):
    doctor_id = fields.Int(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    
    @validates_schema
    def validate_numbers(self, data, **kwargs):
        if data["start_time"] >= data["end_time"]:
            raise ValidationError("Start time must be earlier than end time.")

class AvailableAppointmentSchema(Schema):
    doctor_id = fields.Int(required=False)  # Optional doctor filter
    after_time = fields.DateTime(required=False)  # Optional after_time filter
