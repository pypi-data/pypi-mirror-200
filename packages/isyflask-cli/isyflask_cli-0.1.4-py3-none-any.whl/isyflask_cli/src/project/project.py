from ...globals import Constants
from ..utils.template_gen import generate_flask_template
from ..utils.strings import get_random_string

import typer
from click.types import Choice

app = typer.Typer()

@app.command('init')
def init_project():
    """
    Genera un nuevo proyecto con template para flask
    """
    db_host = ""
    db_user = ""
    db_pass = ""
    db_name = ""
    db_schema = ""
    project_name = typer.prompt("Nombre del proyecto")
    
    dbChoices = Choice([
        Constants.SQLITE_ENGINE.value,
        Constants.SQLSERVER_ENGINE.value,
        Constants.MYSQL_ENGINE.value,
        Constants.POSTGRESQL_ENGINE.value
    ])
    dbDialect: Choice = typer.prompt("Elija su motor de base de datos", "sqlite", show_choices=True, type=dbChoices)
    
    if dbDialect != Constants.SQLITE_ENGINE.value:
        docker_db_enable = typer.confirm("¿Desea agregar configuracion de base de datos para desarrollo local en docker?")
        db_host = typer.prompt("Host de la base de datos")
        db_name = typer.prompt("Nombre de la base de datos")
        db_user = typer.prompt("Usuario de la base de datos")
        
        autopassword = False
        if docker_db_enable is True:
            autopassword = typer.confirm("¿Desea autogenerar la contraseña?")
        if autopassword is True:
            db_pass = get_random_string()
        else:
            db_pass = typer.prompt("Contraseña de la base de datos")
    if dbDialect == "postgresql":
        db_schema = typer.prompt("Nombre del esquema de base de datos")
    
    publish_enable = typer.confirm("¿Desea publicar en un repositorio de contenedores?")
    repository_provider = None
    if publish_enable:
        repository_provider: Choice = typer.prompt("Elija el proveedor de registro de contenedor", "aws", show_choices=True, type=Choice([
            Constants.AWS_REPOSITORY.value,
            Constants.OTHER_REPOSITORY.value
        ]))
    generate_flask_template(project_name, dbDialect, db_host, db_user, db_pass, db_name, db_schema, repository_provider)


    

