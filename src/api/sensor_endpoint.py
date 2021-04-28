import re

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
        parser.add_argument('mac_address', type=self.valid_mac_address)
        return parser

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mac_address', type=self.valid_mac_address)
        return parser

    @staticmethod
    def valid_mac_address(value):
        """Validates mac_address field"""
        if not re.fullmatch(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$", value):
            raise ValueError(f"{value} is not a valid mac address")
        return value
