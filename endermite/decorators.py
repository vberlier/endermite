__all__ = ['public', 'private', 'tag', 'tick', 'load', 'init']


# Visibility decorators


def public(func):
    """Set the visibility of a given function to `public`."""
    return DecoratedFunction.update(func, visibility='public')


def private(func):
    """Set the visibility of a given function to `private`."""
    return DecoratedFunction.update(func, visibility='private')


# Tag decorators


def tag(value):
    """Return a decorator that appends a given tag to a function."""
    def decorator(func):
        """Append the tag to a given function."""
        return DecoratedFunction.append(func, tag=value)
    return decorator


# pylint: disable = invalid-name
tick = tag('minecraft:tick')
load = tag('minecraft:load')
init = tag('endermite:init')


# Underlying class that stores data for the decorated function


class DecoratedFunction:
    """Encapsulate a function to store extra information."""

    def __init__(self, func):
        self.func = func
        self.data = {}

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    @classmethod
    def _decorate(cls, func):
        return func if isinstance(func, cls) else cls(func)

    @classmethod
    def update(cls, func, **kwargs):
        """Update the given key-value pairs."""
        func = cls._decorate(func)
        func.data.update(kwargs)
        return func

    @classmethod
    def append(cls, func, **kwargs):
        """Append each value to a list stored under the associated key."""
        func = cls._decorate(func)
        for key, value in kwargs.items():
            current = func.data.get(key, [])
            current.append(value)
            func.data[key] = current
        return func

    def __repr__(self):
        return f'{self.__class__.__qualname__}({self.func!r}, data={self.data!r})'
