import shutil
import subprocess
from pathlib import Path
from typing import List

import toml
import typer

from pini.config import TEMPLATES_DIR
from pini.setup import python_base


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
    python_base.install_python_base(
        project_name,
        author,
        email,
        init_git,
        init_commitizen,
        init_linters,
        init_pre_commit_hooks,
    )
    typer.echo(f"🚀 Bootstrapping FastAPI project: {project_name}")

    project_path = Path(project_name)

    subprocess.run(
        ["uv", "add", "fastapi", "uvicorn[standard]", "pydantic", "gunicorn"],
        cwd=project_path,
        check=True,
    )

    typer.echo("🔧 Configuring Directory Structure")
    dir_structure: List[Path] = [
        project_path / "app" / "__init__.py",
        project_path / "app" / "api" / "__init__.py",
        project_path / "app" / "models" / "__init__.py",
        project_path / "app" / "utils" / "__init__.py",
        project_path / "tests" / "__init__.py",
        project_path / "tests" / "test_main.py",
    ]

    for path in dir_structure:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    typer.echo("Copying standard configuration files")
    shutil.copytree(
        TEMPLATES_DIR / "frameworks" / "fastapi",
        project_path / ".",
        dirs_exist_ok=True,
    )

    # Add optional ORM setup

    typer.echo("✅ FastAPI project ready!")
