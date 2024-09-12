from datetime import time
from src.extensions import db

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    work_start = db.Column(db.Time, nullable=False)
    work_end = db.Column(db.Time, nullable=False)
    days = db.Column(db.PickleType, nullable=False)  # List of integers [0-6] where 0 = Sunday

    def is_working(self, dt):
        """Check if the doctor is working on a specific date and time."""
        return dt.weekday() in self.days and self.work_start <= dt.time() <= self.work_end


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    doctor = db.relationship('Doctor', backref='appointments')
