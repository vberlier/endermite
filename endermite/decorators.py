__all__ = ['public', 'private', 'tick', 'load', 'init', 'destroy']

from .component_method import ComponentMethod


def public(method):
    """Set the visibility of a given method to `public`."""
    return ComponentMethod.apply(method, visibility='public')


def private(method):
    """Set the visibility of a given method to `private`."""
    return ComponentMethod.apply(method, visibility='private')


def tick(method):
    return ComponentMethod.apply(method, tick=True)


def load(method):
    return ComponentMethod.apply(method, load=True)


def init(method):
    return ComponentMethod.apply(method, init=True)


def destroy(method):
    return ComponentMethod.apply(method, destroy=True)
