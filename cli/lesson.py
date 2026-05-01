import click

from database import get_session
from models import Lesson
from repository import GroupRepository, LessonRepository, SubjectRepository, TeacherRepository
from cli.cli_utils import _ok, _err


@click.group()
def lesson():
    """Управління заняттями."""
    pass


@lesson.command("add")
@click.option("--teacher-id", type=int, prompt="ID викладача")
@click.option("--group-id", type=int, prompt="ID групи")
@click.option("--subject-id", type=int, prompt="ID предмету")
@click.option("--datetime", "datetime_", prompt="Дата і час (YYYY-MM-DD HH:MM)")
@click.option("--room", prompt="Кімната")
def lesson_add(teacher_id, group_id, subject_id, datetime_, room):
    """Додати заняття до розкладу."""
    with get_session() as session:
        teacher = TeacherRepository(session).get(teacher_id)
        group_ = GroupRepository(session).get(group_id)
        subj = SubjectRepository(session).get(subject_id)
        if not teacher:
            _err(f"Викладача ID={teacher_id} не знайдено.")
        if not group_:
            _err(f"Групу ID={group_id} не знайдено.")
        if not subj:
            _err(f"Предмет ID={subject_id} не знайдено.")
        lesson = LessonRepository(session).add(Lesson(teacher, group_, subj, datetime_, room))
        _ok(str(lesson))


@lesson.command("list")
@click.option("--group-id", type=int, default=None, help="Фільтр по групі")
def lesson_list(group_id):
    """Список занять."""
    with get_session() as session:
        repo = LessonRepository(session)
        lessons = repo.get_by_group(group_id) if group_id else repo.get_all()
        if not lessons:
            click.echo("  Занять немає.")
            return
        for lesson in lessons:
            click.echo(f"  {lesson}")


@lesson.command("delete")
@click.argument("lesson_id", type=int)
@click.confirmation_option(prompt="Видалити заняття?")
def lesson_delete(lesson_id):
    """Видалити заняття."""
    with get_session() as session:
        ok = LessonRepository(session).delete(lesson_id)
    if not ok:
        _err(f"Заняття ID={lesson_id} не знайдено.")
    _ok(f"Заняття ID={lesson_id} видалено.")
