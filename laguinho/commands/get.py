import click
import json
import os
import requests

@click.command('get', short_help="Retorna dados do repositório.")
@click.argument('name', required=True, type=str)
def get(name):
    """Retorna os dados disponiveis de um determinado repositório do github."""
    click.echo('Recuperando dados de %s' % name)
    download_dataset('https://api.github.com/repos/ArthurFerrao/bot-casper/contents/backend/src')


def download_dataset(url):
    path = os.getcwd()
    os.mkdir(path+"/teste")
    createDir(url, path+"/teste")


def createDir(url, path):
    req = requests.get(url)
    arqs = json.loads(req.content)
    for arq in arqs:
        if arq["type"] == "dir":
            new_path = path+"/"+arq["name"]
            os.mkdir(new_path)
            createDir(arq["url"], new_path)
        else:
            createFile(arq, path)


def createFile(arq, path):
    file_path = path+'/'+arq["name"]
    open(file_path, 'w').close
