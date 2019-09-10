import os

development = True

if development:
  API_URL = os.getenv('API_URL', 'http://localhost:8080')
else:
  # TODO quando o laguinho estiver hospedado, substituir essa linha
  # API_URL = 'https://laguinho.opendevufcg.org'
  API_URL = os.getenv('API_URL', 'http://localhost:8080')

def set_development():
  global development
  development = True