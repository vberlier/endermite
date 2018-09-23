__all__ = ['Component', 'ComponentBuilder']

from .resource import AutoRegisteringResourceClass, ResourceBuilder
from .component_method import ComponentMethod, ComponentMethodBuilder
from .function import FunctionBuilder, FunctionTagBuilder
from .command import CommandMixin


class ComponentMeta(type):
    def __new__(cls, cls_name, bases, dct, *args, **kwargs):
        methods = dict(cls._extract_methods(dct))

        for base in bases:
            cls._inherit_parent_methods(methods, base)

        dct['component_methods'] = methods
        return super().__new__(cls, cls_name, bases, dct, *args, **kwargs)

    @classmethod
    def _extract_methods(cls, dct):
        defined_members = [name for name in dct if not name.startswith('_')]

        for name in defined_members:
            member = dct[name]
            if isinstance(member, ComponentMethod):
                if member.visibility == 'private':
                    name = '_private/' + name
                yield name, member

    @classmethod
    def _inherit_parent_methods(cls, methods, base):
        for name, method in getattr(base, 'component_methods', {}).items():
            inherited_name = f'{base.name}/{name}'
            methods[inherited_name] = method.inherit(
                inherited_name,
                overwritten=name in methods
            )

    def __init__(cls, cls_name, bases, dct, *args, **kwargs):
        super().__init__(cls_name, bases, dct, *args, **kwargs)
        prefix = f'{cls.namespace}:component/{cls.name}/'

        for name, method in cls.component_methods.items():
            full_name = prefix + name
            method.function_name = full_name
            method.aliases[cls] = full_name

        cls.component_tag = f'{cls.namespace}.component.{cls.name}'
        cls.component_function_attach = f'{cls.namespace}:attach/{cls.name}'
        cls.component_function_detach = f'{cls.namespace}:detach/{cls.name}'


class Component(AutoRegisteringResourceClass, CommandMixin, metaclass=ComponentMeta):
    component_tag = ''
    component_function_attach = ''
    component_function_detach = ''

    def attach(self, component_class):
        if component_class.abstract:
            raise TypeError('Abstract components cannot be attached')
        self.run('function', component_class.component_function_attach)

    def detach(self, component_class):
        if component_class.abstract:
            raise TypeError('Abstract components cannot be detached')
        self.run('function', component_class.component_function_detach)


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
