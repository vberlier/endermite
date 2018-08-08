__all__ = ['Component', 'ComponentBuilder']

from functools import wraps

from .resource import AutoRegisteringResourceClass, ResourceBuilder
from .function import FunctionBuilder, FunctionTagBuilder
from .mixins import CommandMixin
from .decorators import FunctionData
from .utils import wrap_function


class ComponentMeta(type):
    def __new__(cls, cls_name, bases, dct, *args, **kwargs):
        methods = cls._extract_methods(dct)

        for base in bases:
            cls._inherit_parent_methods(methods, base)

        dct['component_methods'] = methods
        return super().__new__(cls, cls_name, bases, dct, *args, **kwargs)

    @classmethod
    def _extract_methods(cls, dct):
        defined_members = [name for name in dct if not name.startswith('_')]
        methods = {}

        for name in defined_members:
            member = dct[name]

            if isinstance(getattr(member, 'data', None), FunctionData):
                if 'visibility' in member.data:
                    wrapper_method = cls._patched_method(member)
                    dct[name] = wrapper_method

                    if member.data['visibility'] == 'private':
                        name = '_private/' + name

                    methods[name] = FunctionData.update_data(
                        member,
                        wrapper=wrapper_method
                    )

        return methods

    @classmethod
    def _patched_method(cls, method):
        @wraps(method)
        def wrapper(self):
            self.run('function', wrapper.data['function_names'][self.__class__])
        return wrapper

    @classmethod
    def _inherit_parent_methods(cls, methods, base):
        for name, method in getattr(base, 'component_methods', {}).items():
            inherited_name = f'{base.name}/{name}'
            inherited_method = wrap_function(method)

            if name not in methods:
                FunctionData.update_data(inherited_method, **method.data)

            methods[inherited_name] = FunctionData.update_data(
                inherited_method,
                visibility=method.data['visibility'],
                wrapper=method.data['wrapper']
            )

    def __init__(cls, cls_name, bases, dct, *args, **kwargs):
        super().__init__(cls_name, bases, dct, *args, **kwargs)
        prefix = f'{cls.namespace}:component/{cls.name}/'

        for name, method in cls.component_methods.items():
            full_name = prefix + name
            FunctionData.update_data(method, function_name=full_name)
            FunctionData.update_data(
                method.data['wrapper'],
                function_names={cls: full_name}
            )

        cls.component_tag = f'{cls.namespace}.component.{cls.name}'
        cls.component_function_attach = f'{cls.namespace}:attach/{cls.name}'
        cls.component_function_detach = f'{cls.namespace}:detach/{cls.name}'


class Component(AutoRegisteringResourceClass, CommandMixin, metaclass=ComponentMeta):
    component_tag = ''
    component_function_attach = ''
    component_function_detach = ''


class ComponentMethodBuilder(ResourceBuilder):
    guard_name = 'component method'

    def build(self):
        function_name = self.resource.data['function_name']
        with FunctionBuilder(self, function_name, []).current() as builder:
            self.resource(self.component_instance)
            builder.build()

        tags = self.resource.data.get('tag', [])

        for name, callback in self.component_callbacks.items():
            if self.resource.data.get(name, False):
                tags.append(callback)

        for tag in tags:
            self.delegate(FunctionTagBuilder, tag, [function_name])


class ComponentBuilder(ResourceBuilder):
    guard_name = 'component'

    def __init__(self, parent, name, resource):
        super().__init__(parent, name, resource)
        self.component_instance = None
        self.component_callbacks = {
            name: f'{self.resource.namespace}:component/callback/{name}/{self.name}'
            for name in ('init', 'destroy', 'tick', 'load')
        }

    def build(self):
        self.component_instance = self.resource(ctx=self.ctx)

        for name, method in self.resource.component_methods.items():
            self.delegate(ComponentMethodBuilder, name, method)

        self.build_attach_function()
        self.build_detach_function()

        for name in ('tick', 'load'):
            callback = self.component_callbacks[name]
            func = self.generate_function([
                f'execute as @e[tag={self.resource.component_tag}] run function #{callback}'
            ])
            self.delegate(FunctionTagBuilder, f'minecraft:{name}', [func])

    def build_attach_function(self):
        func = self.generate_function([
            f'tag @s add {self.resource.component_tag}',
            f'function #{self.component_callbacks["init"]}',
        ])
        self.delegate(FunctionBuilder, self.resource.component_function_attach, [
            f'execute unless entity @s[tag={self.resource.component_tag}] run function {func}',
        ])

    def build_detach_function(self):
        func = self.generate_function([
            f'function #{self.component_callbacks["destroy"]}',
            f'tag @s remove {self.resource.component_tag}',
        ])
        self.delegate(FunctionBuilder, self.resource.component_function_detach, [
            f'execute if entity @s[tag={self.resource.component_tag}] run function {func}',
        ])
