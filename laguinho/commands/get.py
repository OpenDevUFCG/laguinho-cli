import click
import json
import os
import requests


@click.command('get', short_help="Retorna dados do repositório.")
@click.argument('name', required=True, type=str)
def get(name):
    """Retorna os dados disponiveis de um determinado repositório do github."""
    click.echo('Recuperando dados de %s' % name) 
    metadata = { "url": "https://github.com/OpenDevUFCG/laguinho", "path": "/laguinho", "name": "laguinho"}
    download_dataset(metadata)


def request_github_api(url):
    return requests.get(url)


def create_github_api_url(metadata):
    url_params = metadata['url'].split('/')
    server_idx = url_params.index('github.com')
    username = url_params[server_idx + 1]
    repo = url_params[server_idx + 2]

    data_path = metadata['path']
    github_api = "https://api.github.com/repos/{}/{}/contents{}".format(username, repo, data_path)
    return github_api


def download_dataset(metadata):
    current_path = os.getcwd()
    git_url = create_github_api_url(metadata)
    dir_path = current_path +"/" + metadata['name']

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
        create_dir(git_url, dir_path)
        
    else:
        print("Diretório '{}' já existe!".format(metadata['name']))
        metadata['name'] = click.prompt('Qual o nome do novo diretório?')
        download_dataset(metadata)


def create_dir(github_url, dir_path):
    response = request_github_api(github_url)
    contents = json.loads(response.content)

    if  isinstance(contents, list) :

        for content in contents:    
            if content['type'] == 'dir':
                new_dir_path = dir_path + '/' + content['name']
                os.mkdir(new_dir_path)
                new_github_url = github_url + "/" + content['name']
                create_dir(new_github_url, new_dir_path)
            else:
                create_file(content, dir_path)
    else:
        create_file(contents, dir_path)

 
def create_file(content, path):
    download_url = content["download_url"]
    print("criando arquivo", content['name'])

    response = request_github_api(download_url)
    file = open(path + "/" + content['name'], 'w')
    file.write(response.text)
