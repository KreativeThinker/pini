import importlib.resources as pkg_resources
import json
from dataclasses import dataclass
from pathlib import Path

CONFIG_PATH = Path.home() / ".config" / "pinit_config.json"
TEMPLATES_DIR = Path(str(pkg_resources.files("pinit").joinpath("templates")))


@dataclass
class Config:
    author: str
    email: str
    package_managers: dict[str, str]


config: Config = Config(**json.load(CONFIG_PATH.open()))
