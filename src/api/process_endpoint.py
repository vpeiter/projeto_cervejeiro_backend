from flask_restful import reqparse, fields

from models import Process
from .endpoint_mixins import DatabaseMixin,RetrieveMixin, UpdateMixin, DeleteMixin, ListMixin, CreateMixin


class ProcessEndpoint(DatabaseMixin, RetrieveMixin, UpdateMixin, DeleteMixin):
    """Process model endpoint class"""
    entity = Process

    instance_serializer = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def _get_update_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        return parser


class ProcessListEndpoint(DatabaseMixin, ListMixin, CreateMixin):
    entity = Process

    JSON_SCHEMA = {
        'name': str,
        'description': str,
    }

    instance_serializer = {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    }

    def _get_create_parser(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        return parser
