import json
import shutil
import subprocess
from pathlib import Path

import typer

from pini.config import TEMPLATES_DIR


def install_react_vite(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    typer.echo(f"⚡ Bootstrapping React + Vite project: {project_name}")

    subprocess.run(
        [
            "pnpm",
            "create",
            "vite",
            project_name,
            "--template",
            "react-ts",
        ],
        check=True,
    )

    project_path = Path(project_name)

    dev_deps = []
    if init_pre_commit_hooks:
        dev_deps.extend(
            [
                "pre-commit",
                "prettier",
                "prettier-plugin-tailwindcss",
                "prettier-plugin-sort-imports",
            ]
        )
    if init_linters:
        if "prettier" not in dev_deps:
            dev_deps.append("prettier")
    if init_commitizen:
        dev_deps.append("commitizen")

    if dev_deps:
        typer.echo("📦 Installing dev dependencies...")
        subprocess.run(
            [
                "pnpm",
                "add",
                "-D",
            ]
            + dev_deps,
            cwd=project_path,
            check=True,
        )
        typer.echo("✅ Dev dependencies installed.")

    package_json_path = project_path / "package.json"
    with open(package_json_path, "r") as f:
        package_data = json.load(f)

    package_data["author"] = {"name": author, "email": email}

    if "pnpm" not in package_data:
        package_data["pnpm"] = {}
    package_data["pnpm"]["neverBuiltDependencies"] = []

    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)
    typer.echo(
        "✅ Author details and pnpm build settings added to package.json."
    )

    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "vite",
        project_path / ".gitignore",
    )
    typer.echo("✅ .gitignore copied.")

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
        subprocess.run(["pnpm", "cz", "init"], cwd=project_path, check=True)
        typer.echo("✅ Commitizen initialized.")

    if init_pre_commit_hooks:
        typer.echo("⚙️ Setting up pre-commit hooks and Prettier...")
        shutil.copyfile(
            TEMPLATES_DIR / "pre-commit" / "js.yaml",
            project_path / ".pre-commit-config.yaml",
        )
        shutil.copyfile(
            TEMPLATES_DIR / "prettier" / "prettierrc",
            project_path / ".prettierrc",
        )
        shutil.copyfile(
            TEMPLATES_DIR / "prettier" / "prettierignore",
            project_path / ".prettierignore",
        )
        subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)
        typer.echo("✅ Pre-commit hooks installed and Prettier configured.")

    typer.echo("🎉 React + Vite project setup complete!")
