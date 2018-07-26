__all__ = ['Resource']

from collections import defaultdict

from .utils import underscore


class Resource:
    def __init_subclass__(cls, registry=False):
        if registry:
            cls.registry = defaultdict(dict)
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
    def clear_registry(cls):
        if hasattr(cls, 'registry'):
            cls.registry.clear()
