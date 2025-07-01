import typer

from typing import Annotated
from rich import print


app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(
    help="Greet user by [bold red]name[/bold red].",
)
def hello(
    name: Annotated[
        str,
        typer.Argument(help="The name of the person to greet."),
    ],
) -> None:
    print(f"[bold]Hello, [red]{name}[/red]![/bold]")
