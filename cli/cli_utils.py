import sys

import click


def _ok(msg: str) -> None:
    click.echo(click.style(f"  ✓ {msg}", fg="green"))


def _err(msg: str) -> None:
    click.echo(click.style(f"  ✗ {msg}", fg="red"), err=True)
    sys.exit(1)
