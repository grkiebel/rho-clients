import typer
from typing_extensions import Annotated
from typing import Optional, Callable
from click_shell import make_click_shell
from typer import Context, Typer, Argument
from rich import print
from ..api import g_api as apx
from ..cmds.helpers import display_result
from ..cmds.sim import Sim

# ------------------------------------------------------------

intro = "\n Work: Type help to see commands.\nType 'exit' to return to main menu.\n"

sim = Sim()


def make_typer_shell(
    app: Typer,
    prompt: str = "🔳: ",
    intro: str = "\nType help to see commands.\n",
    default: Optional[Callable] = None,
) -> None:
    @app.command(hidden=True)
    def help(ctx: Context, command: Annotated[Optional[str], Argument()] = None):
        print(
            "\n Type 'command --help' or 'help <command>' for help on a specific command."
        )
        if not command:
            ctx.parent.get_help()
            return
        ctx.parent.command.get_command(ctx, command).get_help(ctx)

    @app.command(hidden=True)
    def _default(args: Annotated[Optional[str], Argument()] = None):
        """Default command"""
        if default:
            default(args)
        else:
            print("Command not found. Type 'help' to see commands.")

    @app.callback(invoke_without_command=True)
    def launch(ctx: Context):
        if ctx.invoked_subcommand is None:
            shell = make_click_shell(ctx, prompt=prompt, intro=intro)
            shell.default = _default
            shell.cmdloop()


app: Typer = Typer()
make_typer_shell(app)

# -----[Command Argument Types]-----------------------------


NumOption = Annotated[
    Optional[int], typer.Option("--number", "-n", help="Number of items")
]

IdArg = Annotated[Optional[str], typer.Argument(help="The ID of item")]


# ----[Display Results ]-----------------------------------


def print_list_result(result):
    for item in result:
        fields = [f"{key}: {value}" for key, value in vars(item).items()]
        print(", ".join(fields))
    print(f"Total: {len(result)}")


def print_single_result(result):
    fields = [f"{key}: {value}" for key, value in vars(result).items()]
    print(", ".join(fields))
