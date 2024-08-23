from typer import Typer
import argparse
from ..generated import g_api as apx
from ..log_config import get_logger
from ..generated.g_cmds import (
    tool_app,
    task_app,
    work_app,
    report_app,
    archive_app,
    general_app,
    make_typer_shell,
)

""" This module provides a command shell that can be used 
to accesses the endpoints of the rho-service. """

app: Typer = Typer()
make_typer_shell(app)


app.add_typer(tool_app, name="tools", help="Tool commands")
app.add_typer(task_app, name="tasks", help="Task commands")
app.add_typer(work_app, name="work", help="Work commands")
app.add_typer(report_app, name="reports", help="Report commands")
app.add_typer(archive_app, name="archive", help="Archive commands")
app.add_typer(general_app, name="general", help="General commands")


# @app.command()
# def foobar():
#     "Foobar command"
#     print("-foobar")


def main(service_url: str = None):
    if not service_url:
        service_url = get_args()
    apx.initialize(service_url, get_logger("API-Access"))
    app()


def get_args():
    parser = argparse.ArgumentParser(description="API Generator")
    parser.add_argument(
        "-url",
        "--rho_service_url",
        help="URL to the rho-service",
        default="http://localhost:8080",
    )

    args = parser.parse_args()
    return args.rho_service_url


if __name__ == "__main__":
    main()


# https://dev.to/khumbolamulungu/building-command-line-applications-using-the-click-shell-library-27n3
