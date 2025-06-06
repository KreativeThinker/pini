import json
import shutil
import subprocess
from pathlib import Path

import typer

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def install_nextjs(project_name: str, author: str, email: str):
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
        ],
        check=True,
    )

    project_path = Path(project_name)

    subprocess.run(
        [
            "pnpm",
            "add",
            "-D",
            "prettier",
            "commitizen",
            "pre-commit",
            "prettier-plugin-tailwindcss",
            "prettier-plugin-sort-imports",
        ],
        cwd=project_path,
        check=True,
    )

    package_json_path = project_path / "package.json"
    with open(package_json_path, "r") as f:
        package_data = json.load(f)

    package_data["author"] = {"name": author, "email": email}

    with open(package_json_path, "w") as f:
        json.dump(package_data, f, indent=2)

    shutil.copyfile(
        TEMPLATES_DIR / "pre-commit" / "js.yaml",
        project_path / ".pre-commit-config.yaml",
    )

    shutil.copyfile(
        TEMPLATES_DIR / "gitignore" / "nextjs",
        project_path / ".gitignore",
    )

    shutil.copyfile(
        TEMPLATES_DIR / "prettier" / "prettierrc",
        project_path / ".prettierrc",
    )

    shutil.copyfile(
        TEMPLATES_DIR / "prettier" / "prettierignore",
        project_path / ".prettierignore",
    )

    readme_template = TEMPLATES_DIR / "README.md.tmpl"
    readme_dest = project_path / "README.md"
    readme_dest.write_text(
        readme_template.read_text().replace("{{project_name}}", project_name)
    )

    subprocess.run(["git", "init"], cwd=project_name, check=True)
    subprocess.run(["pnpm", "approve-builds"], cwd=project_path, check=True)
    subprocess.run(["pnpm", "cz", "init"], cwd=project_path, check=True)
    subprocess.run(["pre-commit", "install"], cwd=project_path, check=True)

    typer.echo("✅ Next.js project setup complete!")
