import click

def validate_input(label, type_value, default_value, show_default=True):
    """Recebe um valor como input e retorna uma saida válida.

    A função recebe os parametros para o prompt e, ao receber o input,
    checa se o mesmo é válido, caso seja, retorna o valor.strip(), caso contrário,
    retorna o valor default.

    Args:
        label: Texto a ser visualizado no input.
        type_default: Tipo do input.
        default_value: Valor default caso não seja fornecido qualquer valor ou tenha
    sido fornecido um valor inválido.
        show_default: Flag que diz se o default_value deve ser mostrado.  
    """
    value = click.prompt(label, type=type_value, default=default_value, show_default=show_default)
    if len(value.split(' ')) > 1:
        return default_value

    return default_value if value.strip() == "" else value.strip()


def validate_path(path):
    """Recebe um path e retorna e o valida.
    
    A função recebe um path e verifica se o mesmo termina com '/',
    caso termine, é retornado o path sem o '/' e sem algum espaco no
    comeco ou no final, caso não termine com '/', é tratado apenas a 
    existencia dos espaços.

    Args:
        path: Caminho a ser validado.
    """
    return path[:-1].strip() if path.endswith('/') else path.strip()
