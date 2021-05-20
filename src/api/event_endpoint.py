from datetime import datetime

from flask_restful import reqparse, fields, inputs

from models import Event, EventType, Measurement, Sensor
from .endpoint_mixins import BaseEndpoint, GetMixin, UpdateMixin, DeleteMixin, CreateMixin
from .measurement_endpoint import instance_serializer as measurement_serializer


instance_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.DateTime(dt_format='iso8601'),
    'finish': fields.DateTime(dt_format='iso8601'),
    'duration': fields.DateTime(dt_format='iso8601'),
    'event_type': fields.String,
    'id_process': fields.Integer(default=None),
    'id_sensor': fields.Integer(default=None),
}

detailed_serializer = {
    **instance_serializer,
    'measurements': fields.List(fields.Nested(measurement_serializer))
}


class EventEndpoint(GetMixin, UpdateMixin, DeleteMixin, CreateMixin, BaseEndpoint):
    """Process model endpoint class"""
    entity = Event

    def __init__(self):
        super().__init__(instance_serializer)
        self.detailed_serializer = detailed_serializer

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('finish', type=inputs.datetime_from_iso8601)
        return parser

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.replace_argument('name', type=str, required=True)
        parser.add_argument('start', type=inputs.datetime_from_iso8601)
        parser.add_argument('event_type', type=EventType, required=True)
        parser.add_argument('id_process', type=int, required=True)
        parser.add_argument('finish', type=inputs.datetime_from_iso8601)
        parser.add_argument('duration', type=inputs.timedelta)
        parser.add_argument('id_sensor', type=int)
        return parser

    def _update_instance(self, instance, attributes):
        """Updates instance object using dict of attributes"""
        self._set_instance_attributes(instance, attributes)

    def _create_instance(self, **kwargs):
        """Create instance of entity class given the keyword arguments"""
        event_type = kwargs['event_type']
        self._validate_event_type_arguments(event_type, kwargs)
        if 'start' not in kwargs:
            kwargs['start'] = datetime.now()
        instance = self.entity(**kwargs)
        if instance.id_sensor:
            self._clear_measurements_before_start(instance)
            self._update_existing_measurements(instance)
        return instance

    @classmethod
    def _clear_measurements_before_start(cls, instance):
        """Deletes measurements which belong to event's sensor which are not registered to other events and have
        timestamp before event's start"""
        Measurement.query.filter(Measurement.id_event.is_(None))\
            .filter(Measurement.id_sensor == instance.id_sensor)\
            .filter(Measurement.timestamp < instance.start)\
            .delete()

    @classmethod
    def _update_existing_measurements(cls, instance):
        """Updates measurements' event for measurements which belong to event's sensor which and have timestamp after
        event's start"""
        measurements = Measurement.query.filter(Measurement.id_event.is_(None))\
            .filter(Measurement.id_sensor == instance.id_sensor)\
            .filter(Measurement.timestamp > instance.start)\
            .all()
        instance.measurements = measurements

    @classmethod
    def _validate_event_type_arguments(cls, event_type, arguments):
        """Raises AttributeError if required arguments are missing or not allowed arguments are present for given
        event_type"""
        event_type_attributes = {
            EventType.SENSOR: {
                'required': ['id_sensor'],
                'not_allowed': ['duration']
            },
            EventType.TIMED: {
                'required': ['duration'],
                'not_allowed': ['id_sensor']
            },
            EventType.NORMAL: {
                'required': [],
                'not_allowed': ['id_sensor', 'duration']
            }
        }
        for required in event_type_attributes[event_type]['required']:
            if required not in arguments:
                raise AttributeError(f'{required} is required for event type {event_type}')
        for not_allowed in event_type_attributes[event_type]['not_allowed']:
            if not_allowed in arguments:
                raise AttributeError(f'{not_allowed} is not allowed for event type {event_type}')
