import requests
from ..values import API_URL

API_ENDPOINT = API_URL + "/datasets"

# endpoint: GET /datasets
def get_all():
    """Retorna todos os metadados cadastrados no laguinho API"""
    return requests.get(url=API_ENDPOINT)

# endpoint: GET /datasets/<name>
def get_dataset(dataset_name):
    """Retorna os metadados de um dataset específico pelo nome"""
    endpoint = API_ENDPOINT + '/' + dataset_name
    return requests.get(url=endpoint)

# endpoint: POST /dataset
def post_dataset(metadata):
    """Publica um novo dataset"""
    return requests.post(url=API_ENDPOINT, json=metadata)
