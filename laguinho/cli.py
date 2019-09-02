import click 
import os
import sys

cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))

'''
 buscando os  comandos (arquivos cmd_) e adicionando-os ao grupo do cli principal
Obs: tais métodos são obrigatórios
'''
class laguinhoCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('laguinho.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli

# Iniciando o cli principal, recebendo uma classe para ser instanciada (cls  = LaguinhoCLI)   
@click.command(cls=laguinhoCLI)
def cli():
    """Interface de linha de comando (CLI) para publicar e recuperar dados do laguinho api. """
    pass
