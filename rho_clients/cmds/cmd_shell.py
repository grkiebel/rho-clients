from typer import Typer
from .g_cmds import (
    tool_app,
    task_app,
    work_app,
    report_app,
    archive_app,
    general_app,
    make_typer_shell,
)

# import assignments

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


def main():
    app()


if __name__ == "__main__":
    main()


# https://dev.to/khumbolamulungu/building-command-line-applications-using-the-click-shell-library-27n3
