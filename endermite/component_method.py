__all__ = ['ComponentMethod', 'ComponentMethodBuilder']

from typing import Callable, Dict
from dataclasses import dataclass, field, replace
from functools import wraps, partial

from .resource import ResourceBuilder
from .function import FunctionBuilder, FunctionTagBuilder


@dataclass
class ComponentMethod:
    """Resource that wraps a component method."""

    visibility: str
    tick: bool = False
    load: bool = False
    init: bool = False
    destroy: bool = False
    function: Callable = None
    function_name: str = ''
    aliases: Dict[type, str] = field(default_factory=dict)

    @classmethod
    def apply(cls, method, **kwargs):
        if not isinstance(method, cls):
            return cls(**kwargs, function=method)

        for key, value in kwargs.items():
            setattr(method, key, value)

        return method

    def inherit(self, name, *, overwritten):
        method = replace(self, function_name=name)

        if overwritten:
            method.tick = False
            method.load = False
            method.init = False
            method.destroy = False

        return method

    def __get__(self, component, _component_type):
        return wraps(self.function)(
            partial(self._call_function, *filter(None, [component]))
        )

    def _call_function(self, component):
        component.run('function', self.aliases[type(component)]) # pylint: disable = unsubscriptable-object


class ComponentMethodBuilder(ResourceBuilder):
    guard_name = 'component method'

    def build(self):
        function_name = self.resource.function_name
        function = self.resource.function

        with FunctionBuilder(self, function_name, []).current() as builder:
            identifier = next(self.tag_names)
            selector = f'@e[tag={identifier}]'
            component = self.component_instance

            component.execute(('if', 'entity', selector)).error(
                'Recursive method invocation', f'"{function.__qualname__}()"',
                'in module', f'"{function.__module__}"'
            )

            with component.execute(('unless', 'entity', selector)):
                component.add_tag(identifier)
                with component.execute(('as', selector)) as scope:
                    function(scope)
                component.remove_tag(identifier)

            builder.build()

        for name, callback in self.component_callbacks.items():
            if getattr(self.resource, name):
                self.delegate(FunctionTagBuilder, callback, [function_name])
