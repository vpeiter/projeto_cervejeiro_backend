import re
from enum import Enum

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Process(db.Model):
    __tablename__ = 'process'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)


class EventType(Enum):
    NORMAL = 'NORMAL'
    SENSOR = 'SENSOR'
    TIMED = 'TIMED'

    def __str__(self):
        """String representation of Enum"""
        return str(self.value)


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    finish = db.Column(db.DateTime)
    event_type = db.Column(db.Enum(EventType), nullable=False)
    id_process = db.Column(
        db.Integer,
        db.ForeignKey('process.id', ondelete='RESTRICT', match='FULL'),
        nullable=False
    )

    duration = db.Column(db.Interval)
    id_sensor = db.Column(
        db.Integer,
        db.ForeignKey('sensor.id', ondelete='RESTRICT', match='FULL')
    )

    process = db.relationship('Process', backref=db.backref('events', cascade='all, delete'))
    sensor = db.relationship('Sensor', backref=db.backref('events', cascade='all, delete'))


class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.Text, nullable=False, unique=True)

    @staticmethod
    def valid_mac_address(value):
        """Validates mac_address field"""
        if not re.fullmatch(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", value):
            raise ValueError(f"{value} is not a valid mac address")
        return value


class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    inclination = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    battery = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    id_sensor = db.Column(
        db.Integer,
        db.ForeignKey('sensor.id', ondelete='CASCADE', match='FULL')
    )
    id_event = db.Column(
        db.Integer,
        db.ForeignKey('event.id', ondelete='RESTRICT', match='FULL')
    )

    sensor = db.relationship('Sensor', backref=db.backref('measurements', cascade='all, delete'))
    event = db.relationship('Event', backref=db.backref('measurements', cascade='all, delete'))
