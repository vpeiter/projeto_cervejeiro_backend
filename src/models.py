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

    process = db.relationship('Process', backref='events')
    sensor = db.relationship('Sensor', backref='events')


class Sensor(db.Model):
    __tablename__ = 'sensor'
    id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.Text, nullable=False, unique=True)


class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    inclination = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    battery = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    id_sensor = db.Column(
        db.Integer,
        db.ForeignKey('sensor.id', ondelete='CASCADE', match='FULL'),
        nullable=False
    )
    id_event = db.Column(
        db.Integer,
        db.ForeignKey('event.id', ondelete='RESTRICT', match='FULL'),
        nullable=False
    )

    sensor = db.relationship('Sensor', backref='measurements')
    event = db.relationship('Event', backref='measurements')
