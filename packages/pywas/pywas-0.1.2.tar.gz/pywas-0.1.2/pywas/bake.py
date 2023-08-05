import typer
import yaml
import os

cli = typer.Typer()


@cli.command()
def bake(cmd: str, file: str = "./BakeFile"):
    with open(file) as f:
        cmd_list = yaml.load(f, Loader=yaml.Loader)
    os.system(cmd_list[cmd])


if __name__ == "__main__":
    cli()
