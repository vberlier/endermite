__all__ = ['public', 'private', 'tick', 'load', 'init', 'destroy']

from .component_method import ComponentMethod


def public(method):
    """Make a the method public."""
    return ComponentMethod.apply(method, visibility='public')


def private(method):
    """Make the method private."""
    return ComponentMethod.apply(method, visibility='private')


def tick(method):
    """Make the method execute every tick."""
    return ComponentMethod.apply(method, tick=True)


def load(method):
    """Make the method execute when the datapack loads."""
    return ComponentMethod.apply(method, load=True)


def init(method):
    """Make the method execute when the component gets attached."""
    return ComponentMethod.apply(method, init=True)


def destroy(method):
    """Make the method execute when the component gets detached."""
    return ComponentMethod.apply(method, destroy=True)
