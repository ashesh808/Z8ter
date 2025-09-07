from pathlib import Path
import argparse
import z8ter
from z8ter.cli.create import (
    create_api, create_page
)
from z8ter.cli.run_server import run_server
from z8ter.cli.new import new_project


def main():
    z8ter.set_app_dir(Path.cwd())
    parser = argparse.ArgumentParser(prog="z8", description="Z8ter CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_create = sub.add_parser(
        "create_page",
        help="Create a new page (template + view)"
    )
    p_create.add_argument(
        "name",
        help="Page name (e.g., 'home' or 'app/home')"
    )
    p_new = sub.add_parser(
        "new",
        help="Create a new Z8ter project"
    )
    p_new.add_argument(
        "project_name",
        help="Folder name for the new project"
    )
    p_run = sub.add_parser(
        "run",
        help="Run the app (default: prod)"
    )
    p_run.add_argument(
        "mode", nargs="?",
        choices=["dev", "prod", "WAN", "LAN"],
        help="Use 'dev' for autoreload"
    )
    args = parser.parse_args()
    if args.cmd == "create_page":
        create_page(args.name)
        print("Your new page has been created")
    elif args.cmd == "create_api":
        create_api(args.name)
    elif args.cmd == "new":
        new_project(args.project_name)
    elif args.cmd == "run":
        run_server(mode=args.mode if args.mode else "prod")
    else:
        parser.print_help()
