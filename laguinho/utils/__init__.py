"""É carregado o token do github na variável de ambiente"""
import os
import json
import click

def load_token():
    """Carrega o token do github
    A função verifica se existe o arquivo
    laguinho.config na raiz do usuário, caso
    exista, ele lê o token e retorna, caso não
    exista, é criado e requsitado ao usuário que
    informe um token do github
    """
    config_path = os.path.expanduser('~') + '/laguinho.config'

    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            token = json.load(file)['GITHUB_TOKEN']

    else:
        click.echo('Para baixar os dados do github, é necessário possuir um TOKEN de permissão do Github, caso você não saiba como gerar, siga as instruções desse link.')
        token = click.prompt("Por favor, insira um TOKEN do Github válido").strip()
        file_content = {'GITHUB_TOKEN': token}
        with open(config_path, 'w')  as file:
            json.dump(file_content, file, indent=2)

    return token

os.environ['GITHUB_TOKEN'] = load_token()