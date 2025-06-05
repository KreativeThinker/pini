import shutil
import subprocess
from pathlib import Path

import toml
import typer

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


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
                "tag_format": "$version",
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


def install_fastapi(project_name: str, author: str, email: str):
    typer.echo(f"🚀 Bootstrapping FastAPI project: {project_name}")

    subprocess.run(["uv", "init", project_name], check=True)
    subprocess.run(["uv", "venv"], cwd=project_name, check=True)

    project_path = Path(project_name)

    subprocess.run(
        [
            "uv",
            "add",
            "--dev",
            "pre-commit",
            "black",
            "isort",
            "flake8",
            "commitizen",
        ],
        cwd=project_path,
        check=True,
    )

    subprocess.run(
        ["uv", "add", "fastapi", "uvicorn[standard]", "pydantic"],
        cwd=project_path,
        check=True,
    )

    append_linter_config(project_path / "pyproject.toml")
    insert_author_details(project_path / "pyproject.toml", author, email)

    shutil.copyfile(
        TEMPLATES_DIR / "pre-commit" / "python.yaml",
        project_path / ".pre-commit-config.yaml",
    )

    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "python", project_path / ".gitignore"
    )

    subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)

    typer.echo("✅ FastAPI project ready!")
