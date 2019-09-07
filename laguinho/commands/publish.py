import click
import json
import os

@click.command('publish')
def publish():
    init_laguinho()



def init_laguinho():

    dir_path  = os.getcwd()
    folder_name = os.path.basename(dir_path)

    if os.path.exists(dir_path + "/laguinho.json"):
        click.confirm("\nArquivo laguinho.json já existe. Deseja sobrescrever?", abort=True)
                
    metadata = {}

    metadata['name'] = click.prompt('\nNome do dataset', type=str, default=folder_name)
    metadata['url'] = click.prompt('URL do repositório do Github', type=str)
    metadata['data_format'] = click.prompt("Formato dos arquivos", type=str, default="csv")
    
    data_path = '/' + metadata['name'] + '.' + metadata['data_format']
    metadata['path'] = click.prompt("Caminho dentro do repositório onde está localizado o dataset", type=str, default= data_path)

    maintainers = click.prompt("Mantenedores (separados por virgula)", type=str, default="", show_default=False)
    metadata['maintainers'] = [maintainer.strip() for maintainer in maintainers.split(',') if len(maintainer) > 0]

    metadata['contributable'] = click.confirm("Os dados são contribuíveis?")
   
    click.echo('\nArquivo laguinho.json:\n')

    click.echo( json.dumps(metadata, indent=2))

    if(click.confirm('\n\nOs dados estão corretos?')):
        write_laguinho_json(metadata)
        click.echo('Arquivo criado com sucesso!') 

    else:
        click.echo('Operação cancelada.')


def write_laguinho_json(data):
    file_path = './laguinho.json' 
    with open(file_path, 'w') as fp:
        json.dump(data, fp, indent=2)

