import click
from laguinho.commands.cmd_get import get

@click.group()
def cli():
    """Interface de linha de comando (CLI) para publicar e recuperar dados do laguinho api. """
    pass

cli.add_command(get)

if __name__ == "__main__":
    cli()