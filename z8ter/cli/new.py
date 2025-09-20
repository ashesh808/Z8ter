"""Project scaffolding command for Z8ter.

This module provides the `new_project` entrypoint for the CLI. Currently, it is
a placeholder that directs users to clone the Z8ter repository manually.

Future plans:
  - Generate a minimal project structure (views/, templates/, api/, static/).
  - Support options like --auth, --stripe, etc. for prebuilt scaffolds.
  - Integrate with Jinja2 templates under z8ter/scaffold/.
"""


def new_project(project_name: str) -> None:
    """Scaffold a new Z8ter project (not yet implemented).

    Args:
        project_name: Target folder name for the new project.

    Behavior:
        - Currently prints a friendly message and points to the repo.
        - Future versions will generate a project scaffold into the folder.

    """
    print("⚠️  Project scaffolding is not implemented yet.")
    print(f"You can start your project '{project_name}' by cloning the repo:")
    print("    git clone https://github.com/ashesh808/Z8ter")
