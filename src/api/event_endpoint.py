from flask_restful import reqparse, fields, inputs

from models import Event, EventType
from .endpoint_mixins import BaseEndpoint, GetMixin, UpdateMixin, DeleteMixin, CreateMixin


instance_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'start': fields.DateTime(dt_format='iso8601'),
    'finish': fields.DateTime(dt_format='iso8601'),
    'duration': fields.DateTime(dt_format='iso8601'),
    'event_type': fields.String,
    'id_process': fields.Integer,
    'id_sensor': fields.Integer,
}


class EventEndpoint(GetMixin, UpdateMixin, DeleteMixin, CreateMixin, BaseEndpoint):
    """Process model endpoint class"""
    entity = Event

    def __init__(self):
        super().__init__(instance_serializer)

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('finish', type=inputs.datetime_from_iso8601)
        parser.add_argument('duration', type=inputs.timedelta)
        parser.add_argument('id_sensor', type=int)
        return parser

    def _get_create_parser(self):
        parser = self._get_update_parser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('start', type=inputs.datetime_from_iso8601, required=True)
        parser.add_argument('finish', type=inputs.datetime_from_iso8601)
        parser.add_argument('duration', type=inputs.timedelta)
        parser.add_argument('event_type', type=EventType, required=True)
        parser.add_argument('id_process', type=int, required=True)
        parser.add_argument('id_sensor', type=int)
        return parser
