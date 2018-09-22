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
    aliases: Dict[type, str] = field(default_factory=dict, init=False)

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
        else:
            method.aliases = self.aliases

        return method

    def __get__(self, component, component_type):
        return wraps(self.function)(
            partial(component.run, 'function', self.aliases[component_type])
        )

    def __set__(self, _obj, _value):
        raise AttributeError()


class ComponentMethodBuilder(ResourceBuilder):
    guard_name = 'component method'

    def build(self):
        function_name = self.resource.function_name

        with FunctionBuilder(self, function_name, []).current() as builder:
            self.resource.function(self.component_instance)
            builder.build()

        for name, callback in self.component_callbacks.items():
            if getattr(self.resource, name):
                self.delegate(FunctionTagBuilder, callback, [function_name])
