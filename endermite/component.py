__all__ = ['Component', 'StaticComponent']

from .resource import Resource


class Component(Resource, create_registry=True):
    pass


class StaticComponent(Resource, create_registry=True):
    pass
