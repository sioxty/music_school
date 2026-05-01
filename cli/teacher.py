import click

from database import get_session
from models import Teacher
from repository import TeacherRepository
from cli.cli_utils import _ok, _err


@click.group()
def teacher():
    """Управління викладачами."""
    pass


@teacher.command("add")
@click.option("--name", prompt="Ім'я")
@click.option("--phone", prompt="Телефон")
@click.option("--specialization", prompt="Спеціалізація")
def teacher_add(name, phone, specialization):
    """Додати нового викладача."""
    with get_session() as session:
        repo = TeacherRepository(session)
        t = repo.add(Teacher(name, phone, specialization))
        _ok(t.info())


@teacher.command("list")
def teacher_list():
    """Список усіх викладачів."""
    with get_session() as session:
        teachers = TeacherRepository(session).get_all()
        if not teachers:
            click.echo("  Викладачів немає.")
            return
        for t in teachers:
            click.echo(f"  {t.info()}")


@teacher.command("show")
@click.argument("teacher_id", type=int)
def teacher_show(teacher_id):
    """Деталі викладача за ID."""
    with get_session() as session:
        t = TeacherRepository(session).get(teacher_id)
    if not t:
        _err(f"Викладача ID={teacher_id} не знайдено.")
    click.echo(f"  {t.info()}")


@teacher.command("delete")
@click.argument("teacher_id", type=int)
@click.confirmation_option(prompt="Видалити викладача?")
def teacher_delete(teacher_id):
    """Видалити викладача."""
    with get_session() as session:
        ok = TeacherRepository(session).delete(teacher_id)
    if not ok:
        _err(f"Викладача ID={teacher_id} не знайдено.")
    _ok(f"Викладача ID={teacher_id} видалено.")
