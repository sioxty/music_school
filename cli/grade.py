import click

from database import get_session
from models import Grade
from repository import GradeRepository, LessonRepository, StudentRepository
from cli.cli_utils import _ok, _err


@click.group()
def grade():
    """Управління оцінками."""
    pass


@grade.command("add")
@click.option("--student-id", type=int, prompt="ID учня")
@click.option("--lesson-id", type=int, prompt="ID заняття")
@click.option("--value", type=click.IntRange(1, 12), prompt="Оцінка (1–12)")
@click.option("--comment", default="", prompt="Коментар (Enter — пропустити)")
def grade_add(student_id, lesson_id, value, comment):
    """Виставити оцінку учню."""
    with get_session() as session:
        student = StudentRepository(session).get(student_id)
        lesson_ = LessonRepository(session).get(lesson_id)
        if not student:
            _err(f"Учня ID={student_id} не знайдено.")
        if not lesson_:
            _err(f"Заняття ID={lesson_id} не знайдено.")
        try:
            g = GradeRepository(session).add(Grade(student, lesson_, value, comment))
            _ok(str(g))
        except ValueError as e:
            _err(str(e))


@grade.command("list-student")
@click.argument("student_id", type=int)
def grade_list_student(student_id):
    """Всі оцінки учня."""
    with get_session() as session:
        grades = GradeRepository(session).get_by_student(student_id)
        if not grades:
            click.echo("  Оцінок немає.")
            return
        for g in grades:
            click.echo(f"  {g}")


@grade.command("list-lesson")
@click.argument("lesson_id", type=int)
def grade_list_lesson(lesson_id):
    """Всі оцінки за заняття."""
    with get_session() as session:
        grades = GradeRepository(session).get_by_lesson(lesson_id)
        if not grades:
            click.echo("  Оцінок немає.")
            return
        for g in grades:
            click.echo(f"  {g}")


@grade.command("delete")
@click.argument("grade_id", type=int)
@click.confirmation_option(prompt="Видалити оцінку?")
def grade_delete(grade_id):
    """Видалити оцінку."""
    with get_session() as session:
        ok = GradeRepository(session).delete(grade_id)
    if not ok:
        _err(f"Оцінку ID={grade_id} не знайдено.")
    _ok(f"Оцінку ID={grade_id} видалено.")
