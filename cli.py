import json
from pathlib import Path

import typer
from rich.prompt import Prompt

# Import all new setup modules
from setup import (
    django,
    django_rest_framework,
    fastapi,
    nextjs,
    python_base,
    react_vite,
)

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
        typer.echo("⚠️ Config file not found. Run `pinit config` first.")
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

    # New prompts for optional features
    init_git = (
        Prompt.ask(
            "Initialize git?", choices=["yes", "no"], default="yes"
        ).lower()
        == "yes"
    )
    init_commitizen = (
        Prompt.ask(
            "Initialize commitizen?", choices=["yes", "no"], default="yes"
        ).lower()
        == "yes"
    )
    init_linters = (
        Prompt.ask(
            "Initialize linters/formatters?",
            choices=["yes", "no"],
            default="yes",
        ).lower()
        == "yes"
    )
    init_pre_commit_hooks = (
        Prompt.ask(
            "Initialize pre-commit hooks?",
            choices=["yes", "no"],
            default="yes",
        ).lower()
        == "yes"
    )

    config = json.load(CONFIG_PATH.open())

    if project_type == "fastapi":
        fastapi.install_fastapi(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "nextjs":
        nextjs.install_nextjs(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "react + vite":
        react_vite.install_react_vite(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "django":
        django.install_django(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "django-rest-framework":
        django_rest_framework.install_django_rest_framework(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "python-base":
        python_base.install_python_base(
            project_name,
            config["author"],
            config["email"],
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    else:
        typer.echo("❌ This one isn’t implemented yet")

    typer.echo(f"🎉 Project '{project_name}' bootstrapped successfully!")


if __name__ == "__main__":
    app()
