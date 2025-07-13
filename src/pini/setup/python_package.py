from pathlib import Path

import toml
import typer

from pini.config import TEMPLATES_DIR
from pini.setup.python_base import (
    append_pyproject_section,
    install_python_base,
)


def replace_script_entry(pyproject_path: Path, project_name: str):
    data = toml.load(pyproject_path)
    new_scripts = {project_name: f"{project_name}.__main__:main"}
    if "project" not in data:
        data["project"] = {}
    data["project"]["scripts"] = new_scripts
    with open(pyproject_path, "w") as f:
        toml.dump(data, f)


def install_python_package(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    typer.echo(f"📦 Bootstrapping Python Package project: {project_name}")
    install_python_base(
        project_name=project_name,
        author=author,
        email=email,
        init_git=init_git,
        init_commitizen=init_commitizen,
        init_linters=init_linters,
        init_pre_commit_hooks=init_pre_commit_hooks,
    )

    project_path = Path(project_name)
    project_slug = project_name.lower().replace("-", "_").replace(" ", "_")

    package_path = project_path / "src" / project_slug
    package_path.mkdir(parents=True, exist_ok=True)
    (package_path / "__init__.py").write_text('__version__ = "0.1.0"\n')
    (package_path / "__main__.py").write_text(
        "def main():\n"
        '\tprint("Initialized with PIni!")\n'
        'if __name__ == "__main__":\n'
        "\tmain()"
    )

    append_pyproject_section(
        TEMPLATES_DIR / "pyproject" / "package.toml",
        project_path / "pyproject.toml",
    )

    typer.echo("✅ PyPI packaging enhancements complete.")
