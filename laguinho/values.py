import os

development = True
# TODO quando o laguinho estiver hospedado, substituir essa linha
# API_URL = 'https://laguinho.opendevufcg.org'
API_URL = 'http://localhost:8080'

if development:
    API_URL = os.getenv('LAGUINHO_API_URL', 'http://localhost:8080')

def set_development():
    global development
    development = True
