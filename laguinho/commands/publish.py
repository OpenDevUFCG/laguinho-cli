import click
import json
import os
import requests
from ..values import API_URL

API_ENDPOINT = API_URL + "/datasets"

@click.command('publish', short_help='Publica dataset no laguinho.')
def publish():
    """Publica um dataset no laguinho para que possa ser baixado por outras pessoas por meio do comando get."""
    click.echo('Iniciando publish no laguinho.')
    init_laguinho()
    post_dataset()

def init_laguinho():

    dir_path  = os.getcwd()
    folder_name = os.path.basename(dir_path)

    if os.path.exists(dir_path + "/laguinho.json"):
        click.confirm("\nArquivo laguinho.json já existe. Deseja sobrescrever?")
        return
                
    metadata = {}

    metadata['name'] = click.prompt('\nNome do dataset', type=str, default=folder_name)
    metadata['url'] = click.prompt('URL do repositório do Github', type=str)
    metadata['format'] = click.prompt("Formato dos arquivos", type=str, default="csv")
    
    data_path = '/' + metadata['name'] + '.' + metadata['format']
    metadata['path'] = click.prompt("Caminho dentro do repositório onde está localizado o dataset", type=str, default= data_path)

    maintainers = click.prompt("Mantenedores (separados por virgula)", type=str, default="", show_default=False)
    metadata['maintainers'] = [maintainer.strip() for maintainer in maintainers.split(',') if len(maintainer) > 0]

    metadata['contributable'] = click.confirm("Os dados são contribuíveis?")
   
    click.echo('\nArquivo laguinho.json:\n')

    click.echo( json.dumps(metadata, indent=2))

    if(click.confirm('\n\nOs dados estão corretos?')):
        write_laguinho_json(metadata)
        click.echo('Arquivo criado com sucesso!') 

    else:
        click.echo('Operação cancelada.')

def post_dataset():
    data = read_laguinho_json()
    response = requests.post(url=API_ENDPOINT, json=data)
    if (response.ok):
        click.echo('Sucesso ao publicar o dataset no laguinho!')
    else:
        click.echo('Falha ao publicar o dataset no laguinho')

def read_laguinho_json():
    file_path = './laguinho.json' 
    with open(file_path, 'r') as fp:
        return json.load(fp)

def write_laguinho_json(data):
    file_path = './laguinho.json' 
    with open(file_path, 'w') as fp:
        json.dump(data, fp, indent=2)
