import sys
import secrets
from textwrap import dedent
from keyword import iskeyword
import click

from endermite import Project
from endermite.utils import underscore

from .utils import display_version, load_level_data, project_already_exists
from .config import ENDERMITE_FOLDER_PATH


PROJECT_TEMPLATE = {
    '__init__.py': """
        from endermite import Project, find_resources


        {name} = Project(
            name={name!r},
            project_id={project_id!r},
            description={description!r},
            author={author!r},
            version={version!r},
            **find_resources(__name__)
        )
    """,
    'hello.py': """
        from endermite import StaticComponent
        from endermite.decorators import *


        class Hello(StaticComponent):
            \"""Output `Hello, world!` when the data pack is loaded.\"""

            @load
            @public
            def say_hello(self):
                self.say('Hello, world!')
    """,
}


def identifier(value):
    """Raise a click exception if the input isn't a valid identifier."""
    if not value.isidentifier():
        raise click.BadParameter(f'"{value}" isn\'t a valid python identifier')
    if iskeyword(value) or value in __builtins__:
        raise click.BadParameter(f'"{value}" isn\'t a reasonable identifier')
    if project_already_exists(value):
        raise click.BadParameter(f'"{value}" already exists')
    return value


@click.command()
def init():
    """Create a new endermite project."""
    display_version()
    click.echo('\nCreating a new endermite project.')

    level_data = load_level_data()
    if not level_data:
        sys.exit(1)

    click.echo()

    default_name = underscore(level_data['LevelName'])
    if project_already_exists(default_name):
        default_name = None

    name = click.prompt('Project name', default_name, type=identifier)
    description = click.prompt('Project description', Project.description)
    author = click.prompt('Project author', Project.author)
    version = click.prompt('Project version', Project.version)

    project_id = secrets.token_hex(3)

    project_path = (ENDERMITE_FOLDER_PATH / name).absolute()
    click.echo('\nAbout to create '
               + click.style(str(project_path), fg='blue', bold=True)
               + '.\n')

    if not click.confirm('Is this ok?', default=True):
        raise click.Abort()

    setup_project(name, description, author, version, project_id)
    click.secho('\nDone!', fg='green', bold=True)


def setup_project(name, description, author, version, project_id):
    """Setup an endermite project."""
    project_path = ENDERMITE_FOLDER_PATH / name
    project_path.mkdir(parents=True, exist_ok=True)

    for filename, template in PROJECT_TEMPLATE.items():
        content = dedent(template).strip() + '\n'
        (project_path / filename).write_text(content.format(
            name=name,
            description=description,
            author=author,
            version=version,
            project_id=project_id
        ))
