import json
import shutil
import subprocess
from pathlib import Path

import typer

from pini.config import TEMPLATES_DIR


def install_nextjs(
    project_name: str,
    author: str,
    email: str,
    init_git: bool,
    init_commitizen: bool,
    init_linters: bool,
    init_pre_commit_hooks: bool,
):
    typer.echo(f"⚡ Bootstrapping Next.js project: {project_name}")

    subprocess.run(
        [
            "pnpm",
            "create",
            "next-app",
            project_name,
            "--typescript",
            "--turbopack",
            "--eslint",
            "--tailwind",
            "--app",
            "--src-dir",
            "--import-alias",
            "@/*",
            "--use-pnpm",
            "--no-git",
        ],
        check=True,
    )

    project_path = Path(project_name)

    dev_deps = []
    if init_pre_commit_hooks:
        dev_deps.extend(
            [
                "pre-commit",
                "prettier-plugin-tailwindcss",
                "prettier-plugin-sort-imports",
            ]
        )
    if init_commitizen:
        dev_deps.append("commitizen")
    if init_linters:
        dev_deps.append("prettier")

    if dev_deps:
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

    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)
    typer.echo("✅ Author details added to package.json.")

    if init_pre_commit_hooks:
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

    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "nextjs",
        project_path / ".gitignore",
    )

    readme_template = TEMPLATES_DIR / "README.md.tmpl"
    readme_dest = project_path / "README.md"
    readme_dest.write_text(
        readme_template.read_text().replace("{{project_name}}", project_name)
    )
    typer.echo("✅ README.md generated.")

    if init_git:
        subprocess.run(["git", "init"], cwd=project_name, check=True)
        typer.echo("✅ Git initialized.")

    subprocess.run(["pnpm", "approve-builds"], cwd=project_path, check=True)
    if init_commitizen:
        subprocess.run(["pnpm", "cz", "init"], cwd=project_path, check=True)
        typer.echo("✅ Commitizen initialized.")

    typer.echo("✅ Next.js project setup complete!")
