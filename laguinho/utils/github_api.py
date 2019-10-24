import requests
import json

def create_github_url(metadata, is_file=False):
    """Constrói a URL da API


    Constrói a URL base da API do github a partir
    dos dados presentes no metadata.

    Args:
            metadata: JSON com informações acerca do dataset.
            is_file: FLAG usada pra sinalizar se o dataset é apenas um elemento.
    """
    url_params = metadata['url'].split('/')
    server_idx = url_params.index('github.com')
    username = url_params[server_idx + 1]
    repo = url_params[server_idx + 2]
    data_path = metadata['path']

    return ("https://raw.githubusercontent.com/{}/{}/master{}" if is_file else "https://api.github.com/repos/{}/{}/contents{}").format(username, repo, data_path)


def request_github_api(url):
    """Faz uma requisição a API do Github.


    Faz uma requisição a API do Github.

    Args:
            url: URL do Github a ser requisitada.
    """
    response = requests.get(url)
    return response.content

def verify_github_url(url):
    """Verifica se uma url do Github é válida.

    Verifica se uma url do github é válida, ou seja,
    se existe um repositório referente a essa url fazendo
    uma requisição a mesma.

    Args:
            url: URL de um repositório do Github.
    """
    if 'github.com' not in url:
        return False

    #  Checa se possui o 'github.com', username e repositorio.
    if len(url.split('/')) < 3:
        return False
    
    github_url = create_github_url({ 'url': url, 'path': '/' })
    response = requests.get(url=github_url)
    contents = json.loads(response.content)
    
    return True if isinstance(contents, list) else False
