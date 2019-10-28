import os
import json
import click

@click.command('configure', short_help="Configura o token de autenticação do Github.")
@click.argument('token', required=True, type=str)
def configure(token):
    """Configura o token de autenticação da API do Github"""
    config_path = os.path.expanduser('~') + '/laguinho.config'
    file_content = {'GITHUB_TOKEN':token}

    with open(config_path, 'w')  as file:
        json.dump(file_content, file, indent=2)

    click.echo('Token atualizado!')