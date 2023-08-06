from pathlib import Path

import typer

from .loader import decks_from_directory

app = typer.Typer()


@app.command()
def build(
    source_directory: Path = typer.Option(
        ..., exists=True, file_okay=False, dir_okay=True
    ),
    destination_directory: Path = typer.Option(
        Path("build"),
        exists=False,
        file_okay=False,
        dir_okay=True,
        help="the path of your output/build directory where the pkg files will be generated",
    ),
):
    destination_directory.mkdir(exist_ok=True)
    for deck in decks_from_directory(source_directory):
        deck.write_to_directory(destination_directory)


if __name__ == "__main__":
    app()
