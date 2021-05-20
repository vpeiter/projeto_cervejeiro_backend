import abc

from sqlalchemy.exc import SQLAlchemyError
from flask_restful import abort, Resource, marshal

from models import db


class DatabaseMixin:
    """Mixin for database related methods of endpoints"""
    def __init__(self):
        self._session = db.session

    def _get_instance(self, instance_id):
        """Get instance of entity class by instance_id"""
        return self.entity.query.get_or_404(instance_id)

    def _session_commit(self):
        try:
            self._session.commit()
        except SQLAlchemyError as error:
            self._session.flush()
            self._session.rollback()
            abort(400, message=f"Unable to complete. Error: {error}")


class BaseEndpoint(DatabaseMixin):
    """Base class for all endpoints"""
    def __init__(self, instance_serializer):
        super().__init__()
        self.instance_serializer = instance_serializer
        self.detailed_serializer = self.instance_serializer
    
    def _parse_attributes(self, parser):
        """Returns dict of arguments and values of the request, parsed with given parser. None values are considered as
        absent attributes and ignored."""
        return {argument: value for argument, value in parser.parse_args(strict=True).items() if value is not None}


class ResourceABCMeta(abc.ABCMeta, type(Resource)):
    """"Metaclass for Resource abstract classes"""


class GetMixin(Resource):
    """Mixin to get resources"""
    def get(self, instance_id=None):
        """HTTP GET method"""
        if not instance_id:
            return self.list()
        return self.retrieve(instance_id)

    def retrieve(self, instance_id):
        """Get single instance by instance_id"""
        instance = self._get_instance(instance_id)
        return marshal(instance, self.detailed_serializer)

    def list(self):
        """Get list of instances from entity class"""
        return marshal(self.entity.query.all(), self.instance_serializer)


class CreateMixin(abc.ABC, metaclass=ResourceABCMeta):
    """Mixin to create resources"""
    def post(self):
        """HTTP POST method"""
        attributes = self._parse_attributes(self._get_create_parser())
        try:
            instance = self._create_instance(**attributes)
            self._session.add(instance)
            self._session_commit()
        except AttributeError as error:
            abort(400, message=f"Unable to create instance. Error: {error}")
        return marshal(instance, self.instance_serializer), 201

    def _create_instance(self, **kwargs):
        """Create instance of entity class given the keyword arguments"""
        return self.entity(**kwargs)

    @abc.abstractmethod
    def _get_create_parser(self):
        """Returns parser for create request"""


class UpdateMixin(abc.ABC, metaclass=ResourceABCMeta):
    """Mixin to update resources"""
    def put(self, instance_id):
        """HTTP PUT request"""
        attributes = self._parse_attributes(self._get_update_parser())
        instance = self._get_instance(instance_id)
        self._update_instance(instance, attributes)
        self._session.add(instance)
        self._session_commit()
        return marshal(instance, self.instance_serializer), 201

    def _update_instance(self, instance, attributes):
        """Updates instance object using dict of attributes"""
        self._set_instance_attributes(instance, attributes)

    def _set_instance_attributes(self, instance, attributes):
        """Sets instance attributes given dict of attributes"""
        for attribute in attributes:
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
        """HTTP DELETE method"""
        instance = self._get_instance(instance_id)
        self._delete_instance(instance)
        self._session_commit()
        return '', 204

    def _delete_instance(self, instance_id):
        return self._session.delete(instance_id)

