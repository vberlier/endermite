__all__ = ['Resource']

from collections import defaultdict

from .utils import underscore


class Resource:
    registries = {}

    def __init_subclass__(cls, create_registry=False):
        if create_registry:
            cls.registry = defaultdict(dict)
            cls.registries[cls] = cls.registry
            return

        registry = getattr(cls, 'registry', None)
        if registry is None:
            return

        module = cls.__module__.partition('.')[0]
        name = underscore(cls.__name__)

        resources = registry[module]
        if name in resources:
            raise TypeError(f'{cls.__base__.__name__} "{name}" already exists')
        resources[name] = cls

    @classmethod
    def clear_registries(cls):
        for registry in cls.registries.values():
            registry.clear()
