from datetime import datetime

from flask_restful import reqparse, fields, inputs

from models import DensityCalibration, Measurement
from .endpoint_mixins import BaseEndpoint, GetMixin, CreateMixin


instance_serializer = {
    'id': fields.Integer,
    'coefficient': fields.Float,
    'offset': fields.Float,
    'timestamp': fields.DateTime(dt_format='iso8601'),
    'id_sensor': fields.Integer
}


class DensityCalibrationEndpoint(CreateMixin, GetMixin, BaseEndpoint):
    """Process model endpoint class"""
    entity = DensityCalibration

    def __init__(self):
        super().__init__(instance_serializer)

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('coefficient', type=float, required=True)
        parser.add_argument('offset', type=float, required=True)
        parser.add_argument('timestamp', type=inputs.datetime_from_iso8601)
        parser.add_argument('id_sensor', type=int, required=True)
        return parser

    def _create_instance(self, **kwargs):
        if 'timestamp' not in kwargs:
            kwargs['timestamp'] = datetime.now()
        instance = self.entity(**kwargs)
        self._update_sensor_measurements(instance)
        return instance

    @classmethod
    def _update_sensor_measurements(cls, calibration):
        """Updates density values for all measurements from same sensor with timestamp after calibration's timestamp"""
        Measurement.query.filter(Measurement.id_sensor == calibration.id_sensor)\
            .filter(Measurement.timestamp > calibration.timestamp)\
            .update({'density': (
                Measurement.calculate_density(Measurement.inclination, calibration.coefficient, calibration.offset)
            )})
