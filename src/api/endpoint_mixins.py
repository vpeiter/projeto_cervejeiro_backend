import abc

from flask_restful import abort, Resource, marshal
from sqlalchemy.exc import SQLAlchemyError

from models import db


class DatabaseMixin:
    """Mixin for database related methods of endpoints"""

    def _get_instance(self, instance_id):
        return self.entity.query.get_or_404(instance_id)

    @staticmethod
    def _session_commit():
        try:
            db.session.commit()
        except Exception as error:
            db.session.flush()
            db.session.rollback()
            abort(400, message=f"Unable to create instance. Error: {error}")


class ResourceABCMeta(abc.ABCMeta, type(Resource)):
    """"Metaclass for Resource abstract classes"""


class RetrieveMixin(Resource):
    """Mixin to retrieve resources"""
    def get(self, instance_id):
        instance = self.entity.query.get_or_404(instance_id)
        return marshal(instance, self.instance_serializer)


class ListMixin(Resource):
    """Mixin to retrieve resources"""
    def get(self):
        return marshal(self.entity.query.all(), self.instance_serializer)


class CreateMixin(abc.ABC, metaclass=ResourceABCMeta):
    """Mixin to create resources"""
    def post(self):
        attributes = self._get_create_parser().parse_args(strict=True)
        try:
            instance = self._create_instance(**attributes)
            db.session.add(instance)
            db.session.commit()
        except (AttributeError, SQLAlchemyError) as error:
            abort(400, message=f"Unable to create instance. Error: {error}")
        return marshal(instance, self.instance_serializer), 201

    def _create_instance(self, **kwargs):
        return self.entity(**kwargs)

    @abc.abstractmethod
    def _get_create_parser(self):
        """Returns parser for create request"""


class UpdateMixin(abc.ABC, metaclass=ResourceABCMeta):
    """Mixin to update resources"""
    def put(self, instance_id):
        attributes = self._get_update_parser().parse_args(strict=True)
        instance = self._get_instance(instance_id)
        self._update_instance(instance, attributes)
        self._session_commit()
        return marshal(instance, self.instance_serializer), 201

    def _update_instance(self, instance, attributes):
        for attribute in attributes:
            if not attributes[attribute]:
                continue
            try:
                setattr(instance, attribute, attributes[attribute])
            except AttributeError:
                abort(400, message=f"Unable to set {attribute}")

    @abc.abstractmethod
    def _get_update_parser(self):
        """Returns parser for update request"""


class DeleteMixin(Resource):
    """Mixin to delete resources"""
    def delete(self, instance_id):
        instance = self._get_instance(instance_id)
        self._delete_instance(instance)
        self._session_commit()
        return '', 204

    def _delete_instance(self, instance_id):
        return db.session.delete(instance_id)

