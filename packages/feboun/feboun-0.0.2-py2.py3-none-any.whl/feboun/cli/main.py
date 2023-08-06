import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False, excited: bool = False):
    typer.echo(f"Goodbye {name}")
    if formal:
        typer.echo("Thanks for all the fish.")
    if excited:
        typer.echo("So long and thanks for all the fish!")


if __name__ == "__main__":
    app()
