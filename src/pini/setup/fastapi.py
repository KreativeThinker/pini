import shutil
import subprocess
from pathlib import Path

import toml
import typer

from pini.config import TEMPLATES_DIR


def append_linter_config(pyproject_path: Path):
    config = {
        "tool": {
            "black": {"line-length": 79},
            "isort": {"profile": "black", "line_length": 79},
            "flake8": {
                "max-line-length": 79,
                "extend-ignore": ["E203", "W503"],
            },
            "commitizen": {
                "name": "cz_conventional_commits",
                "tag_format": "v$version",
                "version_scheme": "pep440",
                "version_provider": "uv",
                "update_changelog_on_bump": True,
                "major_version_zero": True,
            },
        }
    }
    data = toml.load(pyproject_path)
    data.update(config)
    with open(pyproject_path, "w") as f:
        toml.dump(data, f)


def insert_author_details(pyproject_path: Path, author: str, email: str):
    data = toml.load(pyproject_path)
    if "project" not in data:
        data["project"] = {}
    data["project"]["authors"] = [{"name": author, "email": email}]
    with open(pyproject_path, "w") as f:
        toml.dump(data, f)


def install_fastapi(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    typer.echo(f"🚀 Bootstrapping FastAPI project: {project_name}")

    subprocess.run(["uv", "init", project_name], check=True)
    subprocess.run(["uv", "venv"], cwd=project_name, check=True)

    project_path = Path(project_name)

    subprocess.run(
        ["uv", "add", "fastapi", "uvicorn[standard]", "pydantic"],
        cwd=project_path,
        check=True,
    )

    if init_linters or init_pre_commit_hooks:
        dev_deps = ["pre-commit"]
        if init_linters:
            dev_deps.extend(["black", "isort", "flake8"])
        if init_commitizen:
            dev_deps.append("commitizen")

        if dev_deps:
            subprocess.run(
                ["uv", "add", "--dev"] + dev_deps,
                cwd=project_path,
                check=True,
            )

    if init_linters:
        append_linter_config(project_path / "pyproject.toml")
        typer.echo("✅ Linters/Formatters configured.")

    insert_author_details(project_path / "pyproject.toml", author, email)

    if init_pre_commit_hooks:
        shutil.copyfile(
            TEMPLATES_DIR / "pre-commit" / "python.yaml",
            project_path / ".pre-commit-config.yaml",
        )
        subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)
        typer.echo("✅ Pre-commit hooks installed.")

    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "python", project_path / ".gitignore"
    )

    if init_git:
        subprocess.run(["git", "init"], cwd=project_name, check=True)
        typer.echo("✅ Git initialized.")

    typer.echo("✅ FastAPI project ready!")
