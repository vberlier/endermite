__all__ = ['Project', 'find_resources']

from typing import List
from dataclasses import dataclass, field
from mcpack import DataPack

from .component import Component, ComponentBuilder
from .function import FunctionBuilder
from .resource import ResourceBuilder
from .utils import import_submodules, name_generator


def find_resources(package):
    """Load the package's submodules and return the defined resources."""
    import_submodules(package)
    return {
        'components': list(Component.registry[package].values()),
    }


@dataclass
class Project:
    """Class representing an endermite project."""

    name: str
    description: str = 'An endermite project'
    author: str = 'N/A'
    version: str = '0.1.0'
    components: List[Component] = field(default_factory=list)

    def build(self):
        """Build the project and return the generated data pack."""
        builder = ProjectBuilder(self.name, self)

        with builder.current():
            builder.build()

        pack = builder.create_data_pack()
        builder.populate(pack)
        return pack


class ProjectBuilder(ResourceBuilder):
    guard_name = 'project'

    def __init__(self, name, resource):
        super().__init__(None, name, resource)
        self.description = ''
        self.function_names = name_generator(f'{self.name}:generated/{{name}}')
        self.tag_names = name_generator(f'{self.name}.generated.{{name}}')

    def build(self):
        self.description = (f'{self.resource.description}\n\n'
                            f'Version {self.resource.version}\n'
                            f'By {self.resource.author}')

        for component in self.resource.components:
            self.delegate(ComponentBuilder, component.name, component)

    def create_data_pack(self):
        return DataPack(self.name, self.description)

    def generate_function(self, commands):
        function_name = next(self.function_names)
        self.delegate(FunctionBuilder, function_name, commands)
        return function_name
