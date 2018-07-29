__all__ = ['Component', 'ComponentBuilder']

from functools import wraps

from .resource import AutoRegisteringResourceClass, ResourceBuilder
from .function import FunctionBuilder
from .mixins import CommandMixin
from .decorators import FunctionData


class Component(AutoRegisteringResourceClass, CommandMixin):
    pass


class ComponentMethodBuilder(ResourceBuilder):
    child_builders = (FunctionBuilder,)
    guard_name = 'component method'

    def build(self):
        full_name = self.resource.data['full_name']
        with FunctionBuilder(self.ctx, full_name, []).current() as builder:
            self.resource()
            builder.build()


def patched_method(self, method, full_name):
    @wraps(method)
    def wrapper():
        self.run('function', full_name)
    return wrapper


class ComponentBuilder(ResourceBuilder):
    child_builders = (ComponentMethodBuilder,)
    guard_name = 'component'

    def build(self):
        instance = self.resource(context=self.ctx)
        methods = {}

        for name in instance.defined_members:
            member = getattr(instance, name)

            if isinstance(getattr(member, 'data', None), FunctionData):
                if 'visibility' in member.data:
                    methods[name] = member
                    self.set_full_name(name, member)
                    setattr(instance, name, patched_method(instance, member,
                                                           member.data['full_name']))

        for name, method in methods.items():
            self.delegate(ComponentMethodBuilder, name, method)

    def set_full_name(self, name, method):
        prefix = f'{self.parent.name}:component/{self.name}/'
        if method.data['visibility'] == 'private':
            name = '_private/' + name
        FunctionData.update_data(method, full_name=prefix + name)
