__all__ = ['Project', 'ProjectBuilder', 'find_resources']

from typing import Dict
from dataclasses import dataclass, field
from mcpack import DataPack

from .component import Component, ComponentBuilder
from .resource import ResourceBuilder
from .utils import import_submodules


def find_resources(package):
    """Load the package's submodules and return the defined resources."""
    import_submodules(package)
    return {
        'components': Component.registry[package].copy(),
    }


@dataclass
class Project:
    """Class representing an endermite project."""

    name: str
    project_id: str
    description: str = 'An endermite project'
    author: str = 'N/A'
    version: str = '0.1.0'
    components: Dict[str, Component] = field(default_factory=dict)

    def build(self):
        """Build the project and return the generated data pack."""
        builder = ProjectBuilder(ProjectBuilder.context(), self.name, self)

        with builder.current():
            builder.build()

        pack = builder.create_data_pack()
        builder.populate(pack)
        return pack


class ProjectBuilder(ResourceBuilder):
    child_builders = (ComponentBuilder,)
    guard_name = 'project'

    def __init__(self, ctx, name, resource):
        super().__init__(ctx, name, resource)
        self.description = ''

    def build(self):
        self.description = (f'{self.resource.description}\n\n'
                            f'Version {self.resource.version}\n'
                            f'By {self.resource.author}')

        for name, resource in self.resource.components.items():
            with ComponentBuilder(self.ctx, name, resource).current() as builder:
                builder.build()

    def create_data_pack(self):
        return DataPack(self.name, self.description)
