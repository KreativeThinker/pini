import json
import subprocess
from pathlib import Path

import typer
from rich.prompt import Prompt

from setup import fastapi

app = typer.Typer()

CONFIG_PATH = Path.home() / ".config" / "pinit_config.json"

frameworks = [
    "react + vite",
    "nextjs",
    "fastapi",
    "django",
    "django-rest-framework",
    "python-base",
]


@app.command()
def init():
    if not CONFIG_PATH.exists():
        typer.echo("⚠️  Config file not found. Run `pinit config` first.")
        raise typer.Exit()
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    typer.echo(f"👋 Hello {config['author']}! Let’s bootstrap a project.")


@app.command()
def config():
    author = typer.prompt("Author name")
    email = typer.prompt("Author email")
    package_managers = {
        "python": typer.prompt(
            "Python package manager (pip/pipenv/poetry/uv)", default="uv"
        ),
        "js": typer.prompt(
            "JS package manager (npm/yarn/pnpm)", default="pnpm"
        ),
    }
    config = {
        "author": author,
        "email": email,
        "package_managers": package_managers,
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    typer.echo("✅ Config saved!")


@app.command()
def create():
    typer.echo("📦 Pick a project type:\n")
    for idx, fw in enumerate(frameworks, 1):
        typer.echo(f"{idx}. {fw}")

    choice = Prompt.ask(
        "\nEnter number",
        choices=[str(i) for i in range(1, len(frameworks) + 1)],
    )
    project_type = frameworks[int(choice) - 1]

    project_name = typer.prompt("📁 Project name")

    config = json.load(CONFIG_PATH.open())

    if project_type == "fastapi":
        fastapi.install_fastapi(
            project_name, config["author"], config["email"]
        )
    else:
        typer.echo("❌ This one isn’t implemented yet")

    git_init = Prompt.ask(
        "Initialize git?", choices=["yes", "no"], default="yes"
    )
    if git_init.lower() == "yes":
        subprocess.run(["git", "init"], cwd=project_name)


if __name__ == "__main__":
    app()
