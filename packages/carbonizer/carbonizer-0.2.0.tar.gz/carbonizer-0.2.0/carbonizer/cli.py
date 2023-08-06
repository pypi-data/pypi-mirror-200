import pathlib
import typing

import typer

from carbonizer import utils, carbon, clipboard

app = typer.Typer()


def wrap_carbonizer(file, exclude, output_folder, rgba, font):
    output = output_folder / ("carbonized_" + file.stem + ".png")
    carbonizer = carbon.Carbonizer(input_file=file,
                                   output_file=output,
                                   exclude=exclude,
                                   background=rgba,
                                   font=font)
    carbonizer()
    return output

@app.command()
def carbonize(
        walk: bool = typer.Option(False, "--walk", "-w"),
        input: str =typer.Argument("."),
        font: str = typer.Option("Night Owl", "--font", "-f"),
        glob_pattern: str = typer.Option("*", "--glob", "-g"),
        output_folder: str = typer.Option(".", "--output-folder", "-t"),
        exclude: str = typer.Option("__pychache__*", "--exclude", "--filter", "-e"),
        copy: bool = typer.Option(False, "--copy", "-c"),
        rgbs: str = typer.Option("0:0:0:0", "--rgbs","--background", help="background in rgba seperated with ':'"),
        dry_run: bool = typer.Option(False, "--dry-run",)
):
    # TODO: Refactor to comply SRP
    # TODO: move file_input as Argument
    file: pathlib.PosixPath
    files: typing.Iterable[pathlib.Path]
    outputs: typing.List[pathlib.Path]
    path = pathlib.Path(input)

    if not path.exists():
        typer.echo(f"No such file or directory - {path}")
        raise typer.Exit()

    if path.is_file():
        files = [path]
    elif walk:
        files = path.rglob(glob_pattern)
    else:
        files = [path.glob(glob_pattern)]

    output_folder = pathlib.Path(output_folder)
    output_folder.mkdir(exist_ok=True)
    rgba = utils.RGBA(*[int(x) for x in rgbs.split(":")])

    outputs = []
    for file in files:
        out = wrap_carbonizer(file,
                              exclude,
                              output_folder,
                              rgba,
                              font)
        outputs.append(out)

    if copy:
        clipboard.Clipboard().copy(outputs[-1])


if __name__ == "__main__":
    typer.run(carbonize)
