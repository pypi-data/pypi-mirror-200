import click

from ..notebooks import launch_jupyter_example


@click.command()
@click.argument("n", type=int)
def run_example(n):
    """Run a QHBayes jupyter notebook example.

    n is the example number; choices are 1"""

    click.echo(f"Running QHBayes Example {n}")

    launch_jupyter_example(n)
