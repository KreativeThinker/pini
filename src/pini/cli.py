import json
import subprocess
from pathlib import Path

import typer
from rich.prompt import Prompt

from pini.config import CONFIG_PATH, Config, load_config

# Import all new setup modules
from pini.setup import (
    django,
    django_rest_framework,
    fastapi,
    nextjs,
    python_base,
    python_package,
    react_vite,
)

app = typer.Typer()


frameworks = [
    "react + vite",
    "nextjs",
    "fastapi",
    "django",
    "django-rest-framework",
    "python-base",
    "python-package",
]


@app.command()
def init():
    if not CONFIG_PATH.exists():
        typer.echo("⚠️ Config file not found. Run `pini configure` first.")
        raise typer.Exit()
    config: Config = load_config()
    typer.echo(f"👋 Hello {config.author}! Let’s bootstrap a project.")


@app.command()
def configure():
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
    if not CONFIG_PATH.exists():
        typer.echo("⚠️ Config file not found. Run `pini configure` first.")
        raise typer.Exit()
    config: Config = load_config()

    typer.echo("📦 Pick a project type:\n")
    for idx, fw in enumerate(frameworks, 1):
        typer.echo(f"{idx}. {fw}")

    choice = Prompt.ask(
        "\nEnter number",
        choices=[str(i) for i in range(1, len(frameworks) + 1)],
    )
    project_type = frameworks[int(choice) - 1]

    project_name = typer.prompt("📁 Project name")
    project_path: Path = Path(project_name)
    if project_path.exists():
        if (
            not Prompt.ask(
                f"⚠️ Project '{project_name}' already exists. Overwrite?",
                choices=["yes", "no"],
                default="no",
            ).lower()
            == "yes"
        ):
            typer.echo("❌ Aborting project creation.")
            raise typer.Exit()
        else:
            typer.echo(f"🗑️ Deleting existing project '{project_name}'...")
            for item in project_path.iterdir():
                if item.is_dir():
                    subprocess.run(["rm", "-rf", str(item)], check=True)
                else:
                    item.unlink()
            project_path.rmdir()

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

    if project_type == "fastapi":
        fastapi.install_fastapi(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "nextjs":
        nextjs.install_nextjs(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "react + vite":
        react_vite.install_react_vite(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "django":
        django.install_django(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "django-rest-framework":
        django_rest_framework.install_django_rest_framework(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "python-base":
        python_base.install_python_base(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    elif project_type == "python-package":
        python_package.install_python_package(
            project_name,
            config.author,
            config.email,
            init_git=init_git,
            init_commitizen=init_commitizen,
            init_linters=init_linters,
            init_pre_commit_hooks=init_pre_commit_hooks,
        )
    else:
        typer.echo("❌ This one isn’t implemented yet")

    if init_git:
        subprocess.run(["git", "add", "."], cwd=project_name, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initialized with PIni"],
            cwd=project_name,
            check=True,
        )
    typer.echo(f"🎉 Project '{project_name}' bootstrapped successfully!")


if __name__ == "__main__":
    app()
