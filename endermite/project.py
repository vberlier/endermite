__all__ = ['Project', 'find_resources']

from typing import List
from dataclasses import dataclass, field
from mcpack import DataPack

from .component import Component, StaticComponent


def find_resources(_package):
    """Inspect a package and return the resources defined in its modules."""

    # FIXME

    return {
        'components': [],
        'static_components': [],
    }


@dataclass
class Project:
    """Class representing an endermite project."""

    name: str
    project_id: str
    description: str = '...'
    author: str = 'N/A'
    version: str = '0.1.0'

    components: List[Component] = field(default_factory=list)
    static_components: List[StaticComponent] = field(default_factory=list)

    def build(self, output_path):
        """Build the project and output the generated data pack."""
        pack = DataPack(
            self.name,
            f'{self.description}\n\nVersion {self.version}\nBy {self.author}'
        )
        pack.dump(output_path, overwrite=True)
