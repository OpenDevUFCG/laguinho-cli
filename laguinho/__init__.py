import click
from .commands.get import get
from .commands.publish import publish
from .commands.configure import configure

@click.group()
def cli():
    """Interface de linha de comando (CLI) para publicar e recuperar dados do laguinho api. """
    pass

cli.add_command(get)
cli.add_command(publish)
cli.add_command(configure)
