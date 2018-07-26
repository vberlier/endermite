__all__ = ['Project', 'find_resources']

from typing import Dict
from dataclasses import dataclass, field
from mcpack import DataPack

from .component import Component, StaticComponent
from .utils import import_submodules


def find_resources(package):
    """Load the package's submodules and return the defined resources."""
    import_submodules(package)
    return {
        'components': Component.registry[package],
        'static_components': StaticComponent.registry[package],
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
    static_components: Dict[str, StaticComponent] = field(default_factory=dict)

    def build(self):
        """Build the project and return the generated data pack."""
        pack = DataPack(
            self.name,
            f'{self.description}\n\nVersion {self.version}\nBy {self.author}'
        )
        return pack
