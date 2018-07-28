__all__ = ['Component', 'ComponentBuilder']

from .resource import AutoRegisteringResourceClass, ResourceBuilder


class Component(AutoRegisteringResourceClass):
    pass


class ComponentBuilder(ResourceBuilder):
    guard_name = 'component'
