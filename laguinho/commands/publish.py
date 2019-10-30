import json
import os
import click
import requests

from ..utils.validations import validate_input, validate_path, validate_github_url
from ..services.datasets import post_dataset

@click.command('publish', short_help='Publica dataset no laguinho.')
def publish():
    """Publica um dataset no laguinho para que possa ser baixado por outras pessoas por meio do comando get."""
    click.echo('Iniciando publish no laguinho.')

    if laguinho_json_exists() and not click.confirm("\nArquivo laguinho.json já existe. Deseja sobrescrever?"):
        publish_dataset()
    else:
        init_laguinho()
        publish_dataset()

def init_laguinho():
    """Cria o arquivo contendo os metadados do dataset

    A função recebe os metadados do dataset e guarda na
    estrutura metadata, após isso, os dados do metadata são
    escritos em um arquivo laguinho.json  no dir atual
    """
    dir_path = os.getcwd()
    folder_name = os.path.basename(dir_path)

    metadata = {}

    metadata['name'] = handle_input(label='\nNome do dataset', type_value=str, default_value=folder_name)

    metadata['url'] = handle_repo_url()

    metadata['format'] = handle_input(label="formato dos arquivos", type_value=str, default_value="csv")

    default_path = '/' + metadata['name'] + '.' + metadata['format']
    data_path = click.prompt("Caminho dentro do repositório onde está localizado o dataset", type=str, default=default_path)
    metadata['path'] = validate_path(data_path)

    maintainers = click.prompt("Mantenedores (separados por virgula)", type=str, default="", show_default=False)
    metadata['maintainers'] = [maintainer.strip() for maintainer in maintainers.split(',') if len(maintainer.strip()) > 0]

    metadata['contributable'] = click.confirm("Os dados são contribuíveis?")

    click.echo('\nArquivo laguinho.json:\n')

    click.echo(json.dumps(metadata, indent=2))

    if click.confirm('\n\nOs dados estão corretos?'):
        write_laguinho_json(metadata)
        click.echo('Arquivo criado com sucesso!')

    else:
        click.echo('Operação cancelada.')


def handle_input(label, type_value, default_value, show_default=True):
    """Recebe o input do usuário

    A função recebe os parametros para o prompt e, ao receber o input,
    checa se o mesmo é válido, caso seja, retorna o valor.strip(), caso contrário,
    retorna o valor default.

    Args:
        label: Texto a ser visualizado no input.
        type_default: Tipo do input.
        default_value: Valor default caso não seja fornecido qualquer valor ou tenha
    sido fornecido um valor inválido.
        show_default: Flag que diz se o default_value deve ser mostrado.
    """
    value = click.prompt(label, type=type_value, default=default_value, show_default=show_default).strip()

    valid_value = validate_input(value)

    while not valid_value:
        click.echo('Valor inválido!\n')
        value = click.prompt(label, type=type_value, default=default_value, show_default=show_default).strip()
        valid_value = validate_input(value)

    return value if value != "" else default_value

def handle_repo_url():
    """Recebe a URL do repositório do Github

    A função recebe a URL do repositório do Github contendo
    o dataset e verifica se a mesma é válida, caso seja, a função
    retorna a mesma, caso não seja válida, a função fica em loop
    requisitando a URL ao usuário até receber uma URL válida
    """
    valid_url = False

    while not valid_url:
        repo_url = click.prompt('URL do repositório do Github', type=str)
        valid_url = validate_github_url(repo_url)
        message = 'URL inválida! Por favor, insira uma URL existente.' if not valid_url else 'URL válida!'
        click.echo(message)

    return repo_url

def laguinho_json_exists():
    """Checa se o arquivo 'laguinho.json' já existe

    A função retorna um booleana que representa
    se o arquivo 'laguinho.json' já existe no dir atual
    """
    dir_path = os.getcwd()
    return os.path.exists(dir_path + "/laguinho.json")

def publish_dataset():
    """Envia os metadados do dataset a API

    A função lê os metadados presentes no arquivo
    laguinho.json e envia os mesmos a API
    """
    data = read_laguinho_json()
    click.echo('Publicando dataset {}'.format(data['name']))
    response = post_dataset(data)
    if response.ok:
        click.echo('Sucesso ao publicar o dataset no laguinho!')
    elif response.status_code == 409:
        click.echo('Nome do dataset já está em uso.')
    else:
        click.echo('Falha ao publicar o dataset no laguinho')

def read_laguinho_json():
    """Retorna o conteúdo do arquivo laguinho.json"""
    file_path = './laguinho.json'
    with open(file_path, 'r') as file:
        return json.load(file)

def write_laguinho_json(data):
    """Escreve os dados recebidos no laguinho.json

    A função recebe um data e escreve-o no arquivo
    'laguinho.json'

    Args:
            data: Representa o conteúdo a ser escrito no
    arquivo 'laguinho.json'
    """
    file_path = './laguinho.json'
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
