import click

from .utils import display_version
from .init import init
from .build import build


def print_version(ctx, _param, value):
    if not value or ctx.resilient_parsing:
        return
    display_version()
    ctx.exit()


@click.group()
@click.option('--version', is_flag=True, is_eager=True, expose_value=False,
              callback=print_version, help='Show the version and exit.')
def ender():
    """Command-line utility to manage endermite projects."""


ender.add_command(init)
ender.add_command(build)
