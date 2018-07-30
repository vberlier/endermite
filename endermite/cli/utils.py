import click
from nbtlib import nbt

import endermite

from .config import (
    MIN_VERSION_ID,
    ENDERMITE_FOLDER_PATH,
    LEVEL_DATA_PATH,
)


# Display utilities


def display_version():
    """Display the endermite version."""
    click.echo(
        click.style('endermite', fg='magenta')
        + click.style(f' v{endermite.__version__}', fg='black', bold=True)
    )


def display_error(message):
    """Display a formatted error message."""
    click.echo(
        '\n' + click.style(' ERR ', fg='white', bg='red') + ' '
        + click.style(message, fg='red', bold=True), err=True
    )


# File-related utilities


def load_level_data():
    """Read the `level.dat` file and return the `Data` compound."""
    try:
        level_data = nbt.load(LEVEL_DATA_PATH, gzipped=True).root['Data']
    except FileNotFoundError:
        display_error(f'Couldn\'t find any "{LEVEL_DATA_PATH}" file. Are you '
                      'sure that the current directory is a minecraft '
                      'world folder?')
    except Exception: # pylint: disable = broad-except
        display_error(f'Couldn\'t load level data "{LEVEL_DATA_PATH}".')
    else:
        world_version = level_data.get('Version', {'Id': 0, 'Name': 'unknown'})

        if MIN_VERSION_ID <= world_version['Id']:
            return level_data

        version_name = world_version['Name']
        display_error(f'Minecraft version "{version_name}" is not compatible '
                      'with endermite.')
    return None


def project_already_exists(project_name):
    """Check if a project already exists."""
    return ((ENDERMITE_FOLDER_PATH / project_name).is_dir()
            or (ENDERMITE_FOLDER_PATH / f'{project_name}.py').is_file())


def public_modules(path):
    """Yield all the paths to public modules in a given directory."""
    for entry in path.iterdir():
        if entry.name.startswith('_'):
            continue
        if entry.is_dir() or entry.is_file() and entry.suffix == '.py':
            yield entry
