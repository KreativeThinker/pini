import importlib.resources as pkg_resources
import json
from dataclasses import dataclass
from pathlib import Path

import typer

CONFIG_PATH = Path.home() / ".config" / "pini_config.json"
TEMPLATES_DIR = Path(str(pkg_resources.files("pini").joinpath("templates")))


@dataclass
class Config:
    author: str
    email: str
    package_managers: dict[str, str]


def load_config() -> Config:
    try:
        with CONFIG_PATH.open() as f:
            return Config(**json.load(f))
    except FileNotFoundError:
        typer.secho(
            "Config not found. Run 'pini configure' first.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)
    except (json.JSONDecodeError, TypeError) as e:
        typer.secho(
            f"Invalid config file format: {e}", fg=typer.colors.RED, err=True
        )
        raise typer.Exit(code=1)
