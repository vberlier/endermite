import click

import endermite


def display_version():
    click.echo(
        click.style('endermite', fg='magenta')
        + click.style(f' v{endermite.__version__}', fg='black', bold=True)
    )
