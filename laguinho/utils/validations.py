import json
import requests

from ..utils.github_api import create_github_url

def validate_input(value):
    """Recebe um valor como input e retorna uma saida válida.

    A função recebe um value e retorna se ele é valido ou não,
    um input não é válido se o mesmo é vazio, ou é um nome
    composto.

    Obs: Esse método está aberto para receber mais validações

    Args:
        value: Valor a ser validado
    """
    # Checa se o input é composto
    if len(value.split(' ')) > 1:
        return False

    return True


def validate_path(path):
    """Recebe um path e retorna um path valido.

    A função recebe um path e verifica se o mesmo termina com '/',
    caso termine, é retornado o path sem o '/' e sem algum espaco no
    comeco ou no final, caso não termine com '/', é tratado apenas a
    existencia dos espaços.

    Args:
        path: Caminho a ser validado.
    """
    return path[:-1].strip() if path.endswith('/') else path.strip()

def validate_github_url(url):
    """Verifica se uma url do Github é válida.

    Verifica se uma url do github é válida, ou seja,
    se existe um repositório referente a essa url fazendo
    uma requisição a mesma.

    Args:
            url: URL de um repositório do Github.
    """
    if 'github.com/' not in url:
        return False

    #  Checa se possui o username (ou organizacão) e repositorio na url.
    url_params = url.split('github.com/')[1]
    if len(url_params.split('/')) < 2:
        return False

    github_url = create_github_url({'url': url, 'path': '/'})
    response = requests.get(url=github_url)
    
    return response.status_code == 200
