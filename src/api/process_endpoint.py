from flask_restful import reqparse, fields

from models import Process
from .endpoint_mixins import BaseEndpoint, GetMixin, UpdateMixin, DeleteMixin, CreateMixin
from .event_endpoint import instance_serializer as event_serializer


instance_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


detailed_serializer = {
    **instance_serializer,
    'events': fields.List(fields.Nested(event_serializer))
}


class ProcessEndpoint(UpdateMixin, DeleteMixin, CreateMixin, GetMixin, BaseEndpoint):
    """Process model endpoint class"""
    entity = Process

    def __init__(self):
        super().__init__(instance_serializer)
        self.detailed_serializer = detailed_serializer

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        return parser

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str)
        return parser
