__all__ = ['AutoRegisteringResourceClass', 'ResourceBuilder', 'clear_registries']

from contextlib import contextmanager
from collections import defaultdict

from .error import build_guard
from .utils import underscore


def clear_registries():
    """Clear all the resource registries."""
    for registry in AutoRegisteringResourceClass.registries:
        registry.clear()


class AutoRegisteringResourceClass:
    """Auto-register class-based project resources when subclassed."""
    registries = []
    name = ''

    def __init_subclass__(cls):
        if cls.__base__ is AutoRegisteringResourceClass:
            cls.registry = defaultdict(dict)
            cls.registries.append(cls.registry)
            return

        registry = getattr(cls, 'registry', None)
        if registry is None:
            return

        module = cls.__module__.partition('.')[0]
        cls.name = underscore(cls.__name__)

        resources = registry[module]
        if cls.name in resources:
            raise TypeError(f'{cls.__base__.__name__} "{cls.name}" already exists')
        resources[cls.name] = cls


class ResourceBuilder(list):
    """Recursive project resource builder."""
    guard_name = 'resource'

    def __init__(self, parent, name, resource):
        super().__init__()
        self.name = name
        self.resource = resource
        self.parent = parent

        if isinstance(parent, ResourceBuilder):
            self.ctx = parent.ctx
            parent.append(self)
        else:
            self.ctx = defaultdict(lambda: None)

    def __getattr__(self, name):
        if self.parent is not None:
            return getattr(self.parent, name)
        raise AttributeError(name)

    @contextmanager
    def current(self):
        """Temporarily set the instance as the current builder of its type."""
        previous = self.ctx[self.__class__]
        self.ctx[self.__class__] = self
        try:
            with build_guard(f'{self.guard_name} "{self.name}"'):
                yield self
        finally:
            self.ctx[self.__class__] = previous

    def build(self):
        """Build the given resource."""

    def delegate(self, builder_class, name, resource):
        """Delegate the building of a sub-resource to a child builder."""
        with builder_class(self, name, resource).current() as builder:
            builder.build()

    def populate(self, pack):
        """Populate the data pack with what was built from the resource."""
        for builder in self:
            builder.populate(pack)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {super().__repr__()})'
