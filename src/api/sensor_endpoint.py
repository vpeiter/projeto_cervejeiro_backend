from flask_restful import reqparse, fields

from models import Sensor
from .endpoint_mixins import DatabaseMixin, GetMixin, UpdateMixin, DeleteMixin, CreateMixin


class SensorEndpoint(DatabaseMixin, GetMixin, UpdateMixin, DeleteMixin, CreateMixin):
    """Sensor model endpoint class"""
    entity = Sensor

    instance_serializer = {
        'id': fields.Integer,
        'mac_address': fields.String
    }

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mac_address', type=Sensor.valid_mac_address)
        return parser

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mac_address', type=Sensor.valid_mac_address)
        return parser
