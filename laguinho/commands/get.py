import click
import requests
import json
import os
import base64


@click.command('get', short_help="Retorna dados do repositório.")
@click.argument('name', required=True, type=str)
def get(name):
    """Retorna os dados disponiveis de um determinado repositório do github."""
    click.echo('Recuperando dados de %s' % name) 
    metadata = { "url": "https://github.com/OpenDevUFCG/laguinho", "path": "/laguinho/commands/get.py", "name": "laguinho"}
    download_dataset(metadata)


def create_github_url(metadata, download_url):
    url_params = metadata['url'].split('/')
    server_idx = url_params.index('github.com')
    username = url_params[server_idx + 1]
    repo = url_params[server_idx + 2]

    data_path = metadata['path']
    url = "https://api.github.com/repos/{}/{}/contents{}".format(username, repo, data_path)
    if(download_url):
        url = "https://raw.githubusercontent.com/{}/{}/master{}".format(username, repo, data_path)
    return url


def download_dataset(metadata):
    current_path = os.getcwd()
    dir_path = current_path +"/" + metadata['name']

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        create(metadata, dir_path)
        
    else:
        print("Diretório '{}' já existe!".format(metadata['name']))
        metadata['name'] = click.prompt('Qual o nome do novo diretório?')
        download_dataset(metadata)

def create(metadata, dir_path):
    url = create_github_url(metadata, False)
    response = request_github_api(url)
    contents = json.loads(response.content)
    if  isinstance(contents, list) :
        create_dir(url, dir_path)
    else:
        name = metadata['path'].split('/').pop()
        url = create_github_url(metadata, True)
        create_file(url, name, dir_path)

def create_dir(github_url, dir_path):
    response = request_github_api(github_url)
    contents = json.loads(response.content)

    for content in contents:    
        if content['type'] == 'dir':
            new_dir_path = dir_path + '/' + content['name']
            os.mkdir(new_dir_path)
            new_github_url = github_url + "/" + content['name']
            create_dir(new_github_url, new_dir_path)
        else:
            create_file(content['download_url'], content['name'], dir_path)

 
def create_file(url, name, path):
    response = request_github_api(url)
    file = open(path + "/" + name, 'wb')
    file.write(response.content)

def request_github_api(url):
    return requests.get(url)