__all__ = ['underscore', 'import_submodules', 'delete_cache']

import sys
import re
from itertools import count
from importlib import import_module
from importlib.resources import contents, is_resource


# String


RE_STRING_PARTS = re.compile(r'[a-z]+|[A-Z][a-z]+|[A-Z]+|[0-9]+')


def underscore(string):
    """Turn a string into a valid snake-cased python identifier."""
    result = '_'.join(RE_STRING_PARTS.findall(string))
    if result[0].isdigit():
        result = '_' + result
    return result.lower()


def name_generator(string):
    for i in count():
        yield string.format(name=f'{i:#08x}'[2:])


# Module


def import_submodules(package):
    """Import all the submodules of a given package."""
    try:
        import_module(package)
        entries = contents(package)
    except Exception: # pylint: disable = broad-except
        return

    for name in entries:
        if name.startswith('_'):
            continue

        if is_resource(package, name):
            if name.endswith('.py'):
                import_module(f'{package}.{name[:-3]}')
        else:
            try:
                contents(f'{package}.{name}')
            except TypeError:
                continue
            import_module(f'{package}.{name}')


def delete_cache(package):
    """Remove a package and all its submodules from the module cache."""
    modules = [mod for mod in sys.modules
               if mod == package or mod.startswith(package + '.')]
    for mod in modules:
        del sys.modules[mod]
