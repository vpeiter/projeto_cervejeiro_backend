from datetime import datetime

from flask_restful import reqparse, fields, inputs

from models import Measurement, Sensor, Event, EventType
from .endpoint_mixins import BaseEndpoint, GetMixin, DeleteMixin, CreateMixin


instance_serializer = {
    'id': fields.Integer,
    'inclination': fields.Float,
    'temperature': fields.Float,
    'battery': fields.Integer,
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'id_sensor': fields.Integer(default=None),
    'id_event': fields.Integer(default=None)
}


class MeasurementEndpoint(GetMixin, DeleteMixin, CreateMixin, BaseEndpoint):
    """Process model endpoint class"""
    entity = Measurement

    def __init__(self):
        super().__init__(instance_serializer)

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sensor_mac_address', type=Sensor.valid_mac_address, required=True)
        parser.add_argument('inclination', type=float, required=True)
        parser.add_argument('temperature', type=float, required=True)
        parser.add_argument('battery', type=float, required=True)
        parser.add_argument('timestamp', type=inputs.datetime_from_iso8601)
        return parser

    def _create_instance(self, **kwargs):
        mac = kwargs.pop('sensor_mac_address')
        sensor = self._get_sensor(mac)
        kwargs["sensor"] = sensor
        if 'timestamp' not in kwargs:
            kwargs['timestamp'] = datetime.now()
        kwargs["event"] = self._get_event(sensor)
        return self.entity(**kwargs)

    def _get_sensor(self, mac_address):
        """Gets sensor by mac_address. Creates new sensor if not found."""
        sensor = Sensor.query.filter_by(mac_address=mac_address).one_or_none()
        if not sensor:
            sensor = Sensor(mac_address=mac_address)
            self._session.add(sensor)
            self._session.flush()
        return sensor

    @classmethod
    def _get_event(cls, sensor):
        """Gets event by sensor"""
        return Event.query.filter(Event.event_type == EventType.SENSOR)\
            .filter(Event.sensor == sensor)\
            .filter(Event.finish.is_(None))\
            .one_or_none()
