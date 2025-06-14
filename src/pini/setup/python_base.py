import shutil
import subprocess
from pathlib import Path

import toml
import typer

from pini.config import TEMPLATES_DIR


def append_pyproject_section(source_path: Path, target_path: Path):
    with open(source_path, "r") as src, open(target_path, "a") as tgt:
        tgt.write("\n")
        tgt.write(src.read())
        tgt.write("\n")


def insert_author_details_python_project(
    pyproject_path: Path, author: str, email: str
):
    data = {}
    if pyproject_path.exists():
        data = toml.load(pyproject_path)
    if "project" not in data:
        data["project"] = {}
    data["project"]["authors"] = [{"name": author, "email": email}]
    with open(pyproject_path, "w") as f:
        toml.dump(data, f)


def install_python_base(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    typer.echo(f"🐍 Bootstrapping Python Base project: {project_name}")

    project_path = Path(project_name)
    project_path.mkdir(parents=True, exist_ok=True)

    typer.echo("Initializing Python environment with uv...")
    subprocess.run(["uv", "init"], cwd=project_path, check=True)
    subprocess.run(["uv", "venv"], cwd=project_path, check=True)
    typer.echo("✅ uv environment initialized.")

    dev_deps = []
    if init_linters or init_pre_commit_hooks:
        dev_deps.append("pre-commit")
        if init_linters:
            dev_deps.extend(["black", "isort", "flake8"])
        if init_commitizen:
            dev_deps.append("commitizen")

    if dev_deps:
        typer.echo("📦 Installing dev dependencies...")
        subprocess.run(
            ["uv", "add", "--dev"] + dev_deps,
            cwd=project_path,
            check=True,
        )
        typer.echo("✅ Dev dependencies installed.")

    # Update pyproject.toml
    pyproject_path = project_path / "pyproject.toml"
    if init_linters:
        typer.echo("⚙️ Configuring linters/formatters...")
        append_pyproject_section(
            TEMPLATES_DIR / "pyproject" / "formatters.toml", pyproject_path
        )
        typer.echo("✅ Linters/Formatters configured.")

    insert_author_details_python_project(pyproject_path, author, email)
    typer.echo("✅ Author details added to pyproject.toml.")

    if init_pre_commit_hooks:
        typer.echo("⚙️ Setting up pre-commit hooks...")
        shutil.copyfile(
            TEMPLATES_DIR / "pre-commit" / "python.yaml",
            project_path / ".pre-commit-config.yaml",
        )
        subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)
        typer.echo("✅ Pre-commit hooks installed.")

    # Copy .gitignore
    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "python",  # Re-use python gitignore
        project_path / ".gitignore",
    )
    typer.echo("✅ .gitignore copied.")

    # Generate README.md
    readme_template = TEMPLATES_DIR / "README.md.tmpl"
    readme_dest = project_path / "README.md"
    readme_dest.write_text(
        readme_template.read_text().replace("{{project_name}}", project_name)
    )
    typer.echo("✅ README.md generated.")

    if init_git:
        typer.echo("Initializing Git repository...")
        subprocess.run(["git", "init"], cwd=project_path, check=True)
        typer.echo("✅ Git initialized.")

    if init_commitizen:
        typer.echo("Initializing Commitizen...")
        append_pyproject_section(
            TEMPLATES_DIR / "pyproject" / "commitizen.toml", pyproject_path
        )
        subprocess.run(["cz", "init"], cwd=project_path, check=True)
        typer.echo("✅ Commitizen initialized.")

    typer.echo("🎉 Python Base project setup complete!")
