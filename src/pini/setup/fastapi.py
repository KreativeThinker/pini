import subprocess
from pathlib import Path

import toml
import typer

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
        ["uv", "add", "fastapi", "uvicorn[standard]", "pydantic"],
        cwd=project_path,
        check=True,
    )

    typer.echo("✅ FastAPI project ready!")
