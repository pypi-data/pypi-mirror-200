"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Mtrain Superclient."""


if __name__ == "__main__":
    main(prog_name="mtrain-superclient")  # pragma: no cover
