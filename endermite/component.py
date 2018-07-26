__all__ = ['Component', 'StaticComponent']

from .resource import Resource


class Component(Resource, registry=True):
    pass


class StaticComponent(Resource, registry=True):
    pass
