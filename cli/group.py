import click

from database import get_session
from models import Group
from repository import GroupRepository, StudentRepository
from cli.cli_utils import _ok, _err


@click.group()
def group():
    """Управління групами."""
    pass


@group.command("add")
@click.option("--name", prompt="Назва групи")
def group_add(name):
    """Створити нову групу."""
    with get_session() as session:
        g = GroupRepository(session).add(Group(name))
        _ok(str(g))


@group.command("list")
def group_list():
    """Список усіх груп."""
    with get_session() as session:
        groups = GroupRepository(session).get_all()
        if not groups:
            click.echo("  Груп немає.")
            return
        for g in groups:
            click.echo(f"  {g}")


@group.command("show")
@click.argument("group_id", type=int)
def group_show(group_id):
    """Деталі групи з переліком учнів."""
    with get_session() as session:
        g = GroupRepository(session).get(group_id)
        if not g:
            _err(f"Групу ID={group_id} не знайдено.")
        click.echo(f"  {g}")
        for s in g.students:
            click.echo(f"    - {s.info()}")


@group.command("add-student")
@click.argument("group_id", type=int)
@click.argument("student_id", type=int)
def group_add_student(group_id, student_id):
    """Додати учня до групи."""
    with get_session() as session:
        repo = GroupRepository(session)
        s_repo = StudentRepository(session)
        group_ = repo.get(group_id)
        student = s_repo.get(student_id)
        if not group_:
            _err(f"Групу ID={group_id} не знайдено.")
        if not student:
            _err(f"Учня ID={student_id} не знайдено.")
        repo.add_student(group_, student)
    _ok(f"Учня ID={student_id} додано до групи ID={group_id}.")


@group.command("remove-student")
@click.argument("group_id", type=int)
@click.argument("student_id", type=int)
def group_remove_student(group_id, student_id):
    """Видалити учня з групи."""
    with get_session() as session:
        repo = GroupRepository(session)
        s_repo = StudentRepository(session)
        group_ = repo.get(group_id)
        student = s_repo.get(student_id)
        if not group_ or not student:
            _err("Групу або учня не знайдено.")
        repo.remove_student(group_, student)
    _ok(f"Учня ID={student_id} видалено з групи ID={group_id}.")


@group.command("delete")
@click.argument("group_id", type=int)
@click.confirmation_option(prompt="Видалити групу?")
def group_delete(group_id):
    """Видалити групу."""
    with get_session() as session:
        ok = GroupRepository(session).delete(group_id)
    if not ok:
        _err(f"Групу ID={group_id} не знайдено.")
    _ok(f"Групу ID={group_id} видалено.")
