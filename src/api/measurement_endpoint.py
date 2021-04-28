from flask_restful import reqparse, fields

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
        'timestamp': fields.DateTime,
        'id_sensor': fields.Integer,
        'id_event': fields.Integer
    }

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sensor_mac_address', type=Sensor.valid_mac_address, required=True)
        parser.add_argument('inclination', type=float, required=True)
        parser.add_argument('temperature', type=float, required=True)
        parser.add_argument('battery', type=float, required=True)
        return parser

    def _create_instance(self, **kwargs):
        mac = kwargs.pop('sensor_mac_address')
        sensor = Sensor.query.filter_by(mac_address=mac).one_or_404()
        kwargs["id_sensor"] = sensor.id
        event = Event.query.filter_by(id_sensor=sensor.id).one_or_404()
        kwargs["id_event"] = event.id
        return self.entity(**kwargs)

