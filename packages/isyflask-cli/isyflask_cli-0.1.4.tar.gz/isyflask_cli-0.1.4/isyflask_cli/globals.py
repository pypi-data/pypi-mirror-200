from enum import Enum
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar, Type, cast, Callable, List
import typer
import toml
from dotenv import load_dotenv

class Constants(Enum):
    FLASK_TEMPLATE = "https://github.com/DavidCuy/flask-pattern"
    SQLITE_ENGINE = "sqlite"
    SQLSERVER_ENGINE = "mssql"
    MYSQL_ENGINE = "mysql"
    POSTGRESQL_ENGINE = "postgresql"
    
    AWS_REPOSITORY = "aws"
    OTHER_REPOSITORY = "other"

T = TypeVar("T")

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_str_to_list(x: Any) -> List[str]:
    assert isinstance(x, str)
    return [x]


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

class BaseConf:
    @property
    def attrs(self) -> List[str]:
        """ Returns a list of the attributes of an object
        Returns:
            List[str]: Attributes
        """
        return list(filter(lambda prop: not str(prop).startswith('_'), self.__dict__.keys()))
    
    @classmethod
    def from_dict(cls_, obj: Any) -> 'Folders':
        assert isinstance(obj, dict)
        
        obj_dict = {}
        attributes = list(filter(lambda prop: not str(prop).startswith('_'), (cls_).__dataclass_fields__.keys()))
        for attr in attributes:
            obj_dict.update({attr: from_str(obj.get(attr))})
        return cls_(**obj_dict)
    
    def to_dict(self):
        output_dict = {}
        for attr in self.attrs:
            output_dict.update({attr: self.__getattribute__(attr)})
        return output_dict
    
    def __repr__(self) -> str:
        """ Model representation
        Returns:
            str: Model output string formatted
        """
        attr_array = [f"{attr}={self.__getattribute__(attr)}" for attr in self.attrs]
        args_format = ",".join(attr_array)
        return f"<{type(self).__name__}({args_format})>"

@dataclass
class Files(BaseConf):
    model: str
    service: str
    controller: str
    endpoint: str

@dataclass
class Folders(BaseConf):
    models: str
    services: str
    controllers: str
    endpoints: str
    root: str

@dataclass
class Definition(BaseConf):
    name: str
    description: str

@dataclass
class Project(BaseConf):
    definition: Definition
    folders: Folders

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        definition = Definition.from_dict(obj.get("definition"))
        folders = Folders.from_dict(obj.get("folders"))
        return Project(definition, folders)

@dataclass
class Template(BaseConf):
    files: Files

    @staticmethod
    def from_dict(obj: Any) -> 'Template':
        assert isinstance(obj, dict)
        files = Files.from_dict(obj.get("files"))
        return Template(files)

@dataclass
class Config(BaseConf):
    project: Project
    template: Template

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        project = Project.from_dict(obj.get("project"))
        template = Template.from_dict(obj.get("template"))
        return Config(project, template)

def load_config(path="isyflask_project.toml") -> Config:
    config_path = Path(path)
    if not config_path.exists():
        typer.echo("config file not found in the project.", color=typer.colors.YELLOW)
        load_dotenv(".env")
        app_name = os.getenv("app_name") or ""
        config_path.write_text(f"""[isyflask.project.definition]
name = "{app_name}"
description = ""

[isyflask.template.files]
model = "templates/isyflask/model.txt"
service = "templates/isyflask/service.txt"
controller = "templates/isyflask/controller.txt"
endpoint = "templates/isyflask/routes.txt"

[isyflask.project.folders]
root = "api"
models = "api/app/Data/Models"
services = "api/app/Services"
controllers = "api/app/Controllers"
endpoints = "api/routes"
        """)
        typer.echo(
            f"Created config file at {config_path} in this path you can find all configuration for the project here.")
        typer.echo(f"Please add the file {config_path} to git tracking and commit it")
    toml_config = toml.loads(config_path.read_text())
    return Config.from_dict(toml_config["isyflask"])