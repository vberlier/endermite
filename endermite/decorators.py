__all__ = ['public', 'private', 'tag', 'tick', 'load', 'init', 'destroy']


def public(func):
    """Set the visibility of a given function to `public`."""
    return FunctionData.update_data(func, visibility='public')


def private(func):
    """Set the visibility of a given function to `private`."""
    return FunctionData.update_data(func, visibility='private')


def tag(value):
    """Return a decorator that appends a given tag to a function."""
    def decorator(func):
        """Append the tag to a given function."""
        return FunctionData.append_data(func, tag=value)
    return decorator


def tick(func):
    return FunctionData.update_data(func, tick=True)


def load(func):
    return FunctionData.update_data(func, load=True)


def init(func):
    return FunctionData.update_data(func, init=True)


def destroy(func):
    return FunctionData.update_data(func, destroy=True)


class FunctionData(dict):
    """Can be attached to a function to store extra information."""

    def update(self, dct):
        for key, value in dct.items():
            if isinstance(value, dict) and isinstance(self.get(key, None), dict):
                FunctionData.update(self[key], value)
                continue
            self[key] = value

    @classmethod
    def _ensure_data(cls, func):
        if not hasattr(func, 'data'):
            func.data = cls()

    @classmethod
    def update_data(cls, func, **kwargs):
        """Update the given key-value pairs."""
        cls._ensure_data(func)
        func.data.update(kwargs)
        return func

    @classmethod
    def append_data(cls, func, **kwargs):
        """Append each value to a list stored under the associated key."""
        cls._ensure_data(func)
        for key, value in kwargs.items():
            current = func.data.get(key, [])
            current.append(value)
            func.data[key] = current
        return func
