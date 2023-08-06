"""Console script for humint."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("humint")
    click.echo("=" * len("humint"))
    click.echo("Intelligence Tools for Humans")


if __name__ == "__main__":
    main()  # pragma: no cover
