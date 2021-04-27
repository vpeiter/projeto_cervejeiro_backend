import json

from flask import request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from sqlalchemy.exc import SQLAlchemyError

from setup import create_app
from models import db, Process, Event, EventType, Sensor, Measurement


app = create_app()
api = Api(app)


instance_serializer = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String
}


class ProcessEndpoint(Resource):
    Entity = Process

    JSON_SCHEMA = {
        'name': str,
        'description': str,
    }

    @property
    def parser(self):
        if not self.parser:
            parser = reqparse.RequestParser()
            for item in self.JSON_SCHEMA:
                parser.add_argument(item, type=self.JSON_SCHEMA[item])
        return self.parser

    @marshal_with(instance_serializer)
    def get(self, instance_id):
        instance = self._get_instance(instance_id)
        return instance

    def delete(self, instance_id):
        instance = self._get_instance(instance_id)
        self._delete_instance(instance)
        self._session_commit()
        return '', 204

    @marshal_with(instance_serializer)
    def put(self, instance_id):
        attributes = self.parser.parse_args(strict=True)
        instance = self._get_instance(instance_id)
        self._update_instance(instance, attributes)
        self._session_commit()
        return instance, 201

    def _get_instance(self, instance_id):
        return self.Entity.query.get_or_404(instance_id)

    def _delete_instance(self, instance_id):
        return db.session.delete(instance_id)

    def _update_instance(self, instance, attributes):
        for attribute in attributes:
            try:
                setattr(instance, attribute, attributes[attribute])
            except AttributeError:
                abort(400, message=f"Unable to set {attribute}")

    @staticmethod
    def _session_commit():
        try:
            db.session.commit()
        except Exception as error:
            db.session.flush()
            db.session.rollback()
            abort(400, message=f"Unable to create instance. Error: {error}")


class ProcessListEndpoint(Resource):
    Entity = Process

    JSON_SCHEMA = {
        'name': str,
        'description': str,
    }

    @property
    def parser(self):
        if not self.parser:
            parser = reqparse.RequestParser()
            for item in self.JSON_SCHEMA:
                parser.add_argument(item, type=self.JSON_SCHEMA[item])
        return self.parser

    @marshal_with(instance_serializer)
    def get(self):
        return self.Entity.query.all()

    @marshal_with(instance_serializer)
    def post(self):
        attributes = self.parser.parse_args(strict=True)
        try:
            instance = self._create_instance(**attributes)
            db.session.add(instance)
            db.session.commit()
        except (AttributeError, SQLAlchemyError) as error:
            abort(400, message=f"Unable to create instance. Error: {error}")
        return instance, 201

    def _create_instance(self, **kwargs):
        return self.Entity(**kwargs)


api.add_resource(ProcessListEndpoint, '/processes')
api.add_resource(ProcessEndpoint, '/processes/<int:process_id>')


if __name__ == '__main__':
    app.run(debug=True)
