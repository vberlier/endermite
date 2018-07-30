__all__ = ['Component', 'ComponentBuilder']

from functools import wraps

from .resource import AutoRegisteringResourceClass, ResourceBuilder
from .function import FunctionBuilder
from .mixins import CommandMixin
from .decorators import FunctionData


def patched_method(method):
    @wraps(method)
    def wrapper(self):
        self.run('function', method.data['function_name'])
    return wrapper


class ComponentMeta(type):
    def __new__(cls, cls_name, bases, dct):
        defined_members = [name for name in dct if not name.startswith('_')]
        methods = {}

        for name in defined_members:
            member = dct[name]

            if isinstance(getattr(member, 'data', None), FunctionData):
                if 'visibility' in member.data:
                    methods[name] = member
                    dct[name] = patched_method(member)

        dct['component_methods'] = methods
        return super().__new__(cls, cls_name, bases, dct)

    def __init__(cls, cls_name, bases, dct):
        super().__init__(cls_name, bases, dct)
        prefix = f'{cls.module}:component/{cls.name}/'

        for name, method in cls.component_methods.items():
            if method.data['visibility'] == 'private':
                name = '_private/' + name
            FunctionData.update_data(method, function_name=prefix + name)


class Component(AutoRegisteringResourceClass, CommandMixin, metaclass=ComponentMeta):
    pass


class ComponentMethodBuilder(ResourceBuilder):
    child_builders = (FunctionBuilder,)
    guard_name = 'component method'

    def build(self):
        function_name = self.resource.data['function_name']
        with FunctionBuilder(self.ctx, function_name, []).current() as builder:
            self.resource(self.parent.instance)
            builder.build()


class ComponentBuilder(ResourceBuilder):
    child_builders = (ComponentMethodBuilder,)
    guard_name = 'component'

    def __init__(self, ctx, name, resource):
        super().__init__(ctx, name, resource)
        self.instance = None

    def build(self):
        self.instance = self.resource(ctx=self.ctx)

        for name, method in self.resource.component_methods.items():
            self.delegate(ComponentMethodBuilder, name, method)
