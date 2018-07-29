__all__ = ['Component', 'ComponentBuilder']

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
        component = self.parent
        prefix = f'{component.parent.name}:component/{component.name}/'

        path = self.name
        if self.resource.data['visibility'] == 'private':
            path = '_private/' + path

        with FunctionBuilder(self.ctx, prefix + path, []).current() as builder:
            self.resource()
            builder.build()


class ComponentBuilder(ResourceBuilder):
    child_builders = (ComponentMethodBuilder,)
    guard_name = 'component'

    def build(self):
        instance = self.resource(context=self.ctx)
        for name in instance.defined_members:
            member = getattr(instance, name)

            if isinstance(getattr(member, 'data', None), FunctionData):
                if 'visibility' in member.data:
                    self.delegate(ComponentMethodBuilder, name, member)
