import click

from database import get_session
from models import Subject
from repository import SubjectRepository
from cli.cli_utils import _ok, _err


@click.group()
def subject():
    """Управління предметами."""
    pass


@subject.command("add")
@click.option("--name", prompt="Назва предмету")
def subject_add(name):
    """Додати предмет."""
    with get_session() as session:
        s = SubjectRepository(session).add(Subject(name))
        _ok(str(s))


@subject.command("list")
def subject_list():
    """Список предметів."""
    with get_session() as session:
        subjects = SubjectRepository(session).get_all()
        if not subjects:
            click.echo("  Предметів немає.")
            return
        for s in subjects:
            click.echo(f"  {s}")


@subject.command("delete")
@click.argument("subject_id", type=int)
@click.confirmation_option(prompt="Видалити предмет?")
def subject_delete(subject_id):
    """Видалити предмет."""
    with get_session() as session:
        ok = SubjectRepository(session).delete(subject_id)
    if not ok:
        _err(f"Предмет ID={subject_id} не знайдено.")
    _ok(f"Предмет ID={subject_id} видалено.")
