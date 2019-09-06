import click
import json

@click.command('publish')
def publish():
    create_form()



def create_form():
    metadats = {}

    metadats['name'] = click.prompt('\nNome do dataset', type=str, default="default")
    metadats['url'] = click.prompt('Url do diretório', type=str)
    metadats['path'] = click.prompt("Caminho da raiz até o diretório onde está o dataset", type=str, default="./")
    maintainers = click.prompt("Mantenedores (separados por virgula)", type=str, default="", show_default=False)
    metadats['data_format'] = click.prompt("Formato do arquivo", type=str, default="csv")
    metadats['contributable'] = click.prompt("Os dados são contribuíveis?" , type=bool, default=True)
   
    metadats['maintainers'] = [maintainer.strip() for maintainer in maintainers.split(',') if len(maintainer) > 0]

    click.echo("\n" + json.dumps(metadats, indent=2))

    if(click.confirm('\n\nOs dados estão corretos?')):
        write_laguinho_json(metadats)
        click.echo('Arquivo criado com sucesso!') 

    else:
        click.echo('Operação cancelada.')


def write_laguinho_json(data):
    file_path = './laguinho.json' 
    with open(file_path, 'w') as fp:
        json.dump(data, fp, indent=2)

