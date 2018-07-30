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
    module = ''
    name = ''

    def __init_subclass__(cls):
        if cls.__base__ is AutoRegisteringResourceClass:
            cls.registry = defaultdict(dict)
            cls.registries.append(cls.registry)
            return

        registry = getattr(cls, 'registry', None)
        if registry is None:
            return

        cls.module = cls.__module__.partition('.')[0]
        cls.name = underscore(cls.__name__)

        resources = registry[cls.module]
        if cls.name in resources:
            raise TypeError(f'{cls.__base__.__name__} "{cls.name}" already exists')
        resources[cls.name] = cls


class ResourceBuilder(list):
    """Recursive project resource builder."""
    parent_builder = None
    child_builders = ()
    guard_name = 'resource'

    def __init_subclass__(cls):
        for builder_class in cls.child_builders:
            builder_class.parent_builder = cls

    @classmethod
    def context(cls):
        """Return an empty build context appropriate for the builder type."""
        ctx = {cls: None}
        for builder_class in cls.child_builders:
            ctx.update(builder_class.context())
        return ctx

    def __new__(cls, ctx, name, resource):
        if cls.parent_builder:
            parent = ctx[cls.parent_builder]
            if parent is None:
                raise TypeError(f'Cannot create {cls.__name__} '
                                f'"{name}", there is no current '
                                f'{cls.parent_builder.__name__}')

            self = super().__new__(cls, ctx, name, resource)
            parent.append(self)
            return self

        return super().__new__(cls, ctx, name, resource)

    def __init__(self, ctx, name, resource):
        super().__init__()
        self.ctx = ctx
        self.name = name
        self.resource = resource
        self.parent = ctx.get(self.parent_builder, None)

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
        with builder_class(self.ctx, name, resource).current() as builder:
            builder.build()

    def populate(self, pack):
        """Populate the data pack with what was built from the resource."""
        if self.__class__.child_builders:
            for builder in self:
                builder.populate(pack)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name!r}, {super().__repr__()})'
