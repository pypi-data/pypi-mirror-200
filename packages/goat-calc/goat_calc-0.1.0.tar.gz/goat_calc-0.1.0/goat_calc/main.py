import typer

app = typer.Typer()

@app.command()
def calc(
    x: int = typer.Argument(..., help="first number"),
    y: int = typer.Argument(..., help="second number"),
    is_add: bool = typer.Option(..., "--add/--sub", help="Set this flag to add. Otherwise, subtract.")
):
    print(x + y if is_add else x - y)

@app.command()
def hello():
    print("hello")
    