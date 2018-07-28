import sys
import time
from importlib import import_module
import click

from endermite import Project
from endermite.resource import clear_registries
from endermite.error import BuildError, crop_traceback_until, print_exc, build_guard
from endermite.utils import delete_cache

from .watch import watch_directory
from .utils import display_version, display_error, load_level_data, public_modules
from .config import ENDERMITE_FOLDER_PATH, DATAPACKS_FOLDER_PATH


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

        try:
            for changes in watch_directory(source_path):
                count = len(changes)
                if count == 1:
                    text = changes[0].format(source_path)
                else:
                    text = f'{count} changes detected'

                now = time.strftime('%H:%M:%S')
                change_time = click.style(now, fg='blue', bold=True)

                click.echo(f'\n{change_time} {text}')

                for module_path in public_modules(source_path):
                    if not build_project(module_path, output_path):
                        break
        except KeyboardInterrupt:
            click.secho('\nExit.', fg='blue', bold=True)
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
        with build_guard(f'module "{project_name}"'):
            module = import_module(project_name)
        project = getattr(module, project_name, None)

        if not isinstance(project, Project):
            click.secho(f'Couldn\'t find any "{project_name}" '
                        'Project object.', fg='black', bold=True)
            return True

        project.build().dump(output_path, overwrite=True)

    except BuildError as exc:
        display_error(f'Couldn\'t build {exc}, traceback below.')
        click.echo()
        exc = exc.__cause__
        crop_traceback_until(exc, module_path)
        print_exc(exc)
        return False

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
        clear_registries()
