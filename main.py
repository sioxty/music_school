import click

from database import init_db
from cli.student import student
from cli.teacher import teacher
from cli.subject import subject
from cli.group import group
from cli.lesson import lesson
from cli.grade import grade
from cli.report import report
from cli.seed import seed


@click.group()
def cli():
    """🎵 Облікова система музичної школи."""
    init_db()


cli.add_command(student)
cli.add_command(teacher)
cli.add_command(subject)
cli.add_command(group)
cli.add_command(lesson)
cli.add_command(grade)
cli.add_command(report)
cli.add_command(seed)


if __name__ == "__main__":
    cli()
