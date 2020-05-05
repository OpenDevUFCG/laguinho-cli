import os
import requests

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

    A função faz uma requisição a API do
    github, para isso ela lê a variável de ambiente
    que possui o oauth token do github e passa
    como parametro no headers da requisição.

    Args:
            url: URL do Github a ser requisitada.
    """
    token = os.environ.get('GITHUB_TOKEN', '')
    response = requests.get(url, headers={"Authorization":  "token " + token})
    return response.content
