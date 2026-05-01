import click

from database import get_session
from models import Student
from repository import StudentRepository
from cli.cli_utils import _ok, _err


@click.group()
def student():
    """Управління учнями."""
    pass


@student.command("add")
@click.option("--name", prompt="Ім'я")
@click.option("--phone", prompt="Телефон")
@click.option("--birth-date", prompt="Дата народження (YYYY-MM-DD)")
def student_add(name, phone, birth_date):
    """Додати нового учня."""
    with get_session() as session:
        repo = StudentRepository(session)
        s = repo.add(Student(name, phone, birth_date))
        _ok(s.info())


@student.command("list")
def student_list():
    """Список усіх учнів."""
    with get_session() as session:
        students = StudentRepository(session).get_all()
        if not students:
            click.echo("  Учнів немає.")
            return
        for s in students:
            click.echo(f"  {s.info()}")


@student.command("show")
@click.argument("student_id", type=int)
def student_show(student_id):
    """Деталі учня за ID."""
    with get_session() as session:
        s = StudentRepository(session).get(student_id)
    if not s:
        _err(f"Учня ID={student_id} не знайдено.")
    click.echo(f"  {s.info()}")


@student.command("delete")
@click.argument("student_id", type=int)
@click.confirmation_option(prompt="Видалити учня?")
def student_delete(student_id):
    """Видалити учня."""
    with get_session() as session:
        ok = StudentRepository(session).delete(student_id)
    if not ok:
        _err(f"Учня ID={student_id} не знайдено.")
    _ok(f"Учня ID={student_id} видалено.")
