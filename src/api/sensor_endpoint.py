from flask_restful import reqparse, fields

from models import Sensor
from .endpoint_mixins import BaseEndpoint, GetMixin, UpdateMixin, DeleteMixin, CreateMixin
from .density_calibration_endpoint import instance_serializer as calibration_serializer


instance_serializer = {
    'id': fields.Integer,
    'mac_address': fields.String
}


detailed_serializer = {
    **instance_serializer,
    'calibrations': fields.List(fields.Nested(calibration_serializer))
}


class SensorEndpoint(GetMixin, UpdateMixin, DeleteMixin, CreateMixin, BaseEndpoint):
    """Sensor model endpoint class"""
    entity = Sensor

    def __init__(self):
        super().__init__(instance_serializer)
        self.detailed_serializer = detailed_serializer

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mac_address', type=Sensor.valid_mac_address)
        return parser

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('mac_address', type=Sensor.valid_mac_address)
        return parser
