__all__ = ['Component', 'ComponentBuilder']

from functools import wraps

from .resource import AutoRegisteringResourceClass, ResourceBuilder
from .function import FunctionBuilder, FunctionTagBuilder
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
        prefix = f'component/{cls.name}/'

        for name, method in cls.component_methods.items():
            if method.data['visibility'] == 'private':
                name = '_private/' + name
            FunctionData.update_data(method, function_name=prefix + name)


class Component(AutoRegisteringResourceClass, CommandMixin, metaclass=ComponentMeta):
    pass


class ComponentMethodBuilder(ResourceBuilder):
    guard_name = 'component method'

    def build(self):
        function_name = f'{self.namespace}:{self.resource.data["function_name"]}'
        with FunctionBuilder(self, function_name, []).current() as builder:
            self.resource(self.component_instance)
            builder.build()

        for name, callback in self.component_callbacks.items():
            if self.resource.data.get(name, False):
                FunctionData.append_data(self.resource, tag=callback)

        tags = self.resource.data.get('tag', [])
        for tag in tags:
            self.delegate(FunctionTagBuilder, tag, [function_name])


class ComponentBuilder(ResourceBuilder):
    guard_name = 'component'

    def __init__(self, parent, name, resource):
        super().__init__(parent, name, resource)
        self.component_instance = None
        self.component_callbacks = {
            'init': f'{self.namespace}:component/callback/init/{self.name}',
            'destroy': f'{self.namespace}:component/callback/destroy/{self.name}',
            'tick': f'{self.namespace}:component/callback/tick/{self.name}',
            'load': f'{self.namespace}:component/callback/load/{self.name}',
        }

    def build(self):
        self.component_instance = self.resource(ctx=self.ctx)

        for name, method in self.resource.component_methods.items():
            self.delegate(ComponentMethodBuilder, name, method)

        component_tag = f'{self.namespace}.component.{self.name}'
        self.build_attach_function(component_tag)
        self.build_detach_function(component_tag)

        for name in ('tick', 'load'):
            callback = self.component_callbacks[name]
            func = self.generate_function([
                f'execute as @e[tag={component_tag}] run function #{callback}'
            ])
            self.delegate(FunctionTagBuilder, f'minecraft:{name}', [func])

    def build_attach_function(self, component_tag):
        function_name = f'{self.namespace}:attach/{self.name}'
        func = self.generate_function([
            f'tag @s add {component_tag}',
            f'function #{self.component_callbacks["init"]}',
        ])
        self.delegate(FunctionBuilder, function_name, [
            f'execute unless entity @s[tag={component_tag}] run function {func}',
        ])

    def build_detach_function(self, component_tag):
        function_name = f'{self.namespace}:detach/{self.name}'
        func = self.generate_function([
            f'function #{self.component_callbacks["destroy"]}',
            f'tag @s remove {component_tag}',
        ])
        self.delegate(FunctionBuilder, function_name, [
            f'execute if entity @s[tag={component_tag}] run function {func}',
        ])
