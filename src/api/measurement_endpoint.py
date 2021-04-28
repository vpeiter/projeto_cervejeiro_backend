from datetime import datetime

from flask_restful import reqparse, fields, inputs

from models import Measurement, Sensor, Event
from .endpoint_mixins import DatabaseMixin, GetMixin, DeleteMixin, CreateMixin


class MeasurementEndpoint(DatabaseMixin, GetMixin, DeleteMixin, CreateMixin):
    """Process model endpoint class"""
    entity = Measurement

    instance_serializer = {
        'id': fields.Integer,
        'inclination': fields.Float,
        'temperature': fields.Float,
        'battery': fields.Integer,
        'timestamp': fields.DateTime(dt_format='iso8601'),
        'id_sensor': fields.Integer,
        'id_event': fields.Integer
    }

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
        if not kwargs['timestamp']:
            kwargs['timestamp'] = datetime.now()
        return self.entity(**kwargs)

    def _get_sensor(self, mac_address):
        """Gets sensor by mac_address. Creates new sensor if not found."""
        sensor = Sensor.query.filter_by(mac_address=mac_address).one_or_none()
        if not sensor:
            sensor = Sensor(mac_address=mac_address)
        return sensor
