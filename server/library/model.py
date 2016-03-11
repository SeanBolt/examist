import flask
from sqlalchemy import Integer
from sqlalchemy.orm import class_mapper, ColumnProperty
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.relationships import RelationshipProperty
from marshmallow import Schema, fields
from server.exc import NotFound
from server.library.util import classproperty
from server.library.schema import create_schema, schema as schemaCreator

class Model(flask.ext.sqlalchemy.Model):
    @classmethod
    def getBy(model, session, **kwargs):
        where = None
        for attr, value in kwargs.iteritems():
            try:
                comp = model.__dict__[attr] == value
            except Exception, e:
                raise AttributeError("Attribute '%s' not found on model '%s'." % (attr, model.__name__))                

            where = comp if where is None else where & comp

        try:
            return session.query(model).filter(where).one()
        except NoResultFound:
            raise NotFound(model.__name__, kwargs)

    @classproperty
    def __schema__(cls):
        if hasattr(cls, "__schema_cache__"):
            return getattr(cls, "__schema_cache__")

        # Create the model schema
        if not cls is Model and issubclass(cls, Model):
            schemaClass = create_schema(cls)
            setattr(cls, "__schema_cache__", schemaClass)
            return schemaClass

    def __json__(self):
        if not hasattr(self, "__schema__"):
            raise RuntimeError("Model %s has no schema defined. Make sure the @bind_schema decorator has been called.")

        data = {}
        ins = inspect(self)

        # Don't try to access the unloaded keys or we'll trigger some
        # lazy loading.
        attrs = set(ins.attrs.keys()) - ins.unloaded 

        for name in attrs:
            data[name] = getattr(self, name)

        return self.__schema__().dump(data).data

    @classmethod
    def __declare_last__(cls):
        cls.__schema__