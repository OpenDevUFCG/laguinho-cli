import click
from commands.cmd_get import get 

# Iniciando o cli principal, recebendo uma classe para ser instanciada (cls  = LaguinhoCLI)   
@click.group()
def cli():
    """Interface de linha de comando (CLI) para publicar e recuperar dados do laguinho api. """
    pass

cli.add_command(get)

if __name__ == "__main__":
    cli()