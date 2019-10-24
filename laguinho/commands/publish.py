import json
import os
import click
import requests

from ..utils.github_api import validate_github_url
from ..utils.validation import validate_input, validate_path
from ..values import API_URL

API_ENDPOINT = API_URL + "/datasets"

@click.command('publish', short_help='Publica dataset no laguinho.')
def publish():
    """Publica um dataset no laguinho para que possa ser baixado por outras pessoas por meio do comando get."""
    click.echo('Iniciando publish no laguinho.')
    init_laguinho()
    if  laguinho_json_exists():
        post_dataset()

def init_laguinho():
    """Cria o arquivo contendo os metadados do dataset

    A função recebe os metadados do dataset e guarda na
    estrutura metadata, após isso, os dados do metadata são
    escritos em um arquivo laguinho.json  no dir atual
    """
    dir_path = os.getcwd()
    folder_name = os.path.basename(dir_path)

    if laguinho_json_exists():
        click.confirm("\nArquivo laguinho.json já existe. Deseja sobrescrever?")
        return

    metadata = {}

    metadata['name'] = validate_input(label='\nNome do dataset', type_value=str, default_value=folder_name)
    metadata['url'] = recv_repo_url()

    metadata['format'] = validate_input(label="formato dos arquivos", type_value=str, default_value="csv")

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


def recv_repo_url():
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

def post_dataset():
    """Envia os metadados do dataset a API

    A função lê os metadados presentes no arquivo
    laguinho.json e envia os mesmos a API
    """
    data = read_laguinho_json()
    response = requests.post(url=API_ENDPOINT, json=data)
    if response.ok:
        click.echo('Sucesso ao publicar o dataset no laguinho!')
    else:
        click.echo('Falha ao publicar o dataset no laguinho')

def read_laguinho_json():
    """Retorna o conteúdo do arquivo laguinho.json"""
    file_path = './laguinho.json'
    with open(file_path, 'r') as fp:
        return json.load(fp)

def write_laguinho_json(data):
    """Escreve os dados recebidos no laguinho.json

    A função recebe um data e escreve-o no arquivo
    'laguinho.json'

    Args:
            data: Representa o conteúdo a ser escrito no
    arquivo 'laguinho.json'
    """
    file_path = './laguinho.json'
    with open(file_path, 'w') as fp:
        json.dump(data, fp, indent=2)
