import click

from database import init_db, seed_demo_data


@click.group()
def seed():
    """Інструменти для наповнення бази даних."""
    pass


@seed.command("demo")
def seed_demo():
    """Заповнити базу даних демонстраційними даними."""
    init_db()
    seed_demo_data()
    click.echo("Демонстраційні дані успішно додано до бази.")
