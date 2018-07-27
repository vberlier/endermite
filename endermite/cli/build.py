import sys
import time
from traceback import print_exception
from importlib import import_module
import click

from endermite import Project
from endermite.resource import Resource
from endermite.utils import delete_cache

from .utils import display_version, display_error, load_level_data, public_modules
from .config import ENDERMITE_FOLDER_PATH, DATAPACKS_FOLDER_PATH


def print_exc(exc):
    """Display an exception."""
    print_exception(exc.__class__, exc, exc.__traceback__)


@click.command()
@click.option('--watch', is_flag=True, help='Rebuild on file changes.')
def build(watch):
    """Build all the projects of the current world."""
    display_version()
    click.echo('\nBuilding endermite projects.')

    if not load_level_data():
        sys.exit(1)

    source_path = ENDERMITE_FOLDER_PATH.absolute()
    output_path = DATAPACKS_FOLDER_PATH.absolute()

    if not source_path.is_dir():
        display_error('The "@endermite" directory does not exist.')
        sys.exit(1)

    sys.path.append(str(source_path))

    if watch:
        formatted_dir = click.style(str(source_path), fg='blue', bold=True)
        click.echo(f'\nWatching directory {formatted_dir}.')

        # FIXME
    else:
        for module_path in public_modules(source_path):
            if not build_project(module_path, output_path):
                sys.exit(1)


def build_project(module_path, output_path):
    """Build a project and dump the data pack in the given directory."""
    start_time = time.perf_counter()
    project_name = module_path.stem

    click.echo(f'\nAttempting to build "{project_name}"...')

    try:
        module = import_module(project_name)
        project = getattr(module, project_name, None)

        if not isinstance(project, Project):
            click.secho(f'Couldn\'t find any "{project_name}" '
                        'Project object.', fg='black', bold=True)
            return True

        project.build().dump(output_path, overwrite=True)

    except Exception as exc: # pylint: disable = broad-except
        display_error('Build failed, traceback below.')
        click.echo()
        print_exc(exc)
        return False

    else:
        build_time = time.perf_counter() - start_time
        click.secho('Done! ', fg='green', bold=True, nl=False)
        click.secho(f'(took {build_time:.3f}s)',
                    fg='black', bold=True)
        return True

    finally:
        delete_cache(project_name)
        Resource.clear_registries()
