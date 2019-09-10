import click
import json
import os
import requests


## IMPORTANTE!! Refatorar codigo
## Da pra testar chamando a funcao download_dataset, passando name como sendo o path do github do repo, além de um metadata tipo {"path":"/", "name":"laguinho"}, por exemplo
@click.command('get', short_help="Retorna dados do repositório.")
@click.argument('name', required=True, type=str)
def get(name):
    """Retorna os dados disponiveis de um determinado repositório do github."""
    click.echo('Recuperando dados de %s' % name)


# Refatorar -> caso a url n venha com o http pode dar ruim
# Retorna a url do repositorio na api do github
def create_github_api_url(metadata):
    url_params = metadata['url'].split('/')
    username =  url_params[3] 
    repo =  url_params[4]
    data_path = metadata['path']
    github_api = "https://api.github.com/repos/{}/{}/contents{}".format(username, repo, data_path)
    return github_api


# Funcao principal que chama o createDir, alem de criar a pasta onde ficaram os arquivos baixados
def download_dataset(metadata):
    path = metadata['path']
    current_path = os.getcwd()
    git_url = create_github_api_url(metadata)
    dir_path = current_path + path + metadata['name']
    os.mkdir(dir_path)
    createDir(git_url, dir_path)

# Funcao recursiva que checa se o elemento é um dir ou não. Caso seja um arquivo, ele chama a funcao
# de criar um novo arquivo, caso contrário, ele itera dentro dos arquivos do diretorio, onde caso o arquivo
# seja um dir, ele cria a pasta para ele, além de chamar a funcao recursivamente atualizando os paths
def createDir(github_url, dir_path):
    response = requests.get(github_url)
    contents = json.loads(response.content)

    if  "type" not in contents :
        # o contents é um diretorio
        for content in contents:    
            if content['type'] == 'dir':
                dir_path = dir_path + '/' + content['name']
                os.mkdir(dir_path)

            new_github_url = github_url + "/" + content['name']
            createDir(new_github_url, dir_path)

    else:
        createFile(contents, dir_path)

# Recebe o content, faz uma requisicao pegando o conteudo dele e escreve no arquivo local
## IMPORTANTE -> o download_url ta retornando bits, precisa converter pra string 
def createFile(content, path):
    download_url = content["download_url"]
    response = requests.get(download_url)
    file = open(path + "/" + content['name'], 'w')
    file.write(str(response.content)).close()
