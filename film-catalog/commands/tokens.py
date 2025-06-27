import typer

from rich import print
from typing import Annotated

from api.api_v1.auth.services import redis_tokens


app = typer.Typer(
    name="tokens",
    help="Tokens management command.",
    rich_markup_mode="rich",
    no_args_is_help=True,
)


@app.command(
    help="Check if [bold red]token[/bold red] is valid - exists or not.",
)
def check(
    token: Annotated[
        str,
        typer.Argument(help="Your token to check"),
    ],
):
    print(
        f"Token: [bold]{token}[/bold]",
        (
            "[bold green]exists[/bold green]"
            if redis_tokens.token_exists(token)
            else f"[bold red]doesn't exist[/bold red]"
        ),
    )
