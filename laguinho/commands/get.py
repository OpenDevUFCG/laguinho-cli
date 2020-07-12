import json
import os
import click
from ..utils.github_api import create_github_url, request_github_api
from ..services.datasets import get_dataset

@click.command('get', short_help="Retorna dados do repositório.")
@click.argument('name', required=True, type=str)
def get(name):
    """Retorna os dados disponiveis de um determinado repositório do github."""
    click.echo('Recuperando dados de %s' % name)

    response = get_dataset(name)

    if response.status_code == 200:
        metadata = json.loads(response.content)
        try:
            download_dataset(metadata)
            click.echo("\nArquivo(s) baixado(s) com sucesso!\n")
        except:
            click.echo('\nVocê alcançou sua cota máxima de downloads disponíveis pelo Github.\n')
    else:
        click.echo('\nNome não condiz com nenhum dataset cadastrado.\n')


def download_dataset(metadata):
    """Baixa os arquivos do github


    Baixa os arquivos através da API do Github.

    Args:
            metadata: JSON com informações acerca do dataset.
    """
    current_path = os.getcwd()
    dir_path = "{}/{}".format(current_path, metadata['name'])

    if not os.path.isdir(dir_path):
        mkdir_and_cd(dir_path)
        check_dataset(metadata)

    else:
        click.echo("Diretório '{}' já existe!".format(metadata['name']))
        metadata['name'] = click.prompt('Qual o nome do novo diretório?')
        download_dataset(metadata)

def check_dataset(metadata):
    """ Checa o dataset


    Verifica se o elemento específicado no atributo path é um diretório ou um
    arquivo. Caso seja um diretório, é chamada a função create, caso contrário,
    o arquivo é criado.

    Args:
            metadata: JSON com informações acerca do dataset.
    """
    github_url = create_github_url(metadata)
    response = request_github_api(github_url)
    contents = json.loads(response)
    if  isinstance(contents, list):
        create(contents, github_url)
    else:
        name = metadata['path'].split('/').pop()
        donwload_url = create_github_url(metadata, True)
        create_file(donwload_url, name)

def create(contents, github_url):
    """ Cria os elementos do dataset


   Recebe um ou mais elementos. Caso o elemento
   seja um diretório, é chamada a função para criação
   de diretórios, caso contrário, é chamada a de criação
   de arquivo.

    Args:
            contents: Elementos a ser analisado.
            github_url: URL  base do github usada na criação
            dos repositórios.

    """
    for content in contents:
        if content['type'] == 'dir':
            create_dir(github_url, content)
        else:
            create_file(content['download_url'], content['name'])

def create_dir(github_url, content):
    """Cria um diretório

    Cria um diretório do dataset utilizando as biblioteca
    'so'. Após a criação, é chamada a função 'create' passando
    os elementos dentro do respectivo diretório criado.

    Args:
            github_url: URL  base do github usada na criação
            dos repositórios.

            content: Elemento retornado pela API do github
            referente ao diretório a ser criado.

    """
    click.echo("Criando diretório {}".format(content['name']))
    dir_path = "{}/{}".format(os.getcwd(), content['name'])
    mkdir_and_cd(dir_path)
    new_github_url = "{}/{}".format(github_url, content['name'])
    response = request_github_api(new_github_url)
    contents = json.loads(response)
    create(contents, new_github_url)

def create_file(donwload_url, name):
    """Cria um arquivo específico


    Baixa e cria um novo arquivo do dataset.

    Args:
            download_url: URL da API para o download do arquivo.
            name: Nome do arquivo.
    """
    click.echo("Criando arquivo {}".format(name))
    content = request_github_api(donwload_url)
    with open("{}/{}".format(os.getcwd(), name), 'wb') as file:
        file.write(content)

def mkdir_and_cd(dir_path):
    """Cria e entra em um determinado diretório"""
    os.mkdir(dir_path)
    os.chdir(dir_path)
