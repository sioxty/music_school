"""
reports.py — форматовані звіти для адміністратора.

Звіти використовують репозиторії, а не сесію напряму.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from repository import GradeRepository, GroupRepository, LessonRepository, StudentRepository, SubjectRepository

_SEP   = "─" * 62
_THICK = "═" * 62


def _header(title: str) -> str:
    return f"\n{_THICK}\n  {title}\n{_THICK}"


def _grade_word(value: float) -> str:
    if value >= 10:
        return "відмінно"
    if value >= 7:
        return "добре"
    if value >= 4:
        return "задовільно"
    return "незадовільно"


# ---------------------------------------------------------------------------
# Звіт 1: успішність учня
# ---------------------------------------------------------------------------

def report_student(session: Session, student_id: int) -> str:
    student_repo = StudentRepository(session)
    grade_repo   = GradeRepository(session)

    student = student_repo.get(student_id)
    if not student:
        return f"  Учня з ID={student_id} не знайдено."

    grades = grade_repo.get_by_student(student_id)

    lines = [_header(f"Успішність учня: {student.name}")]
    lines.append(f"  Дата народження: {student.birth_date}")
    lines.append(_SEP)

    if not grades:
        lines.append("  Оцінок ще немає.")
        return "\n".join(lines)

    for g in grades:
        comment = f"  ↳ {g.comment}" if g.comment else ""
        lines.append(
            f"  {g.lesson.datetime_}  {g.lesson.subject.name:<20}"
            f"  {g.value:>2}/12  ({g.grade_label():<14})"
            f"  Викл.: {g.lesson.teacher.name}"
        )
        if comment:
            lines.append(f"    {comment}")

    avg = grade_repo.average_by_student(student_id) or 0
    lines.append(_SEP)
    lines.append(
        f"  Оцінок: {len(grades)}   "
        f"Середній бал: {avg:.1f}/12  ({_grade_word(avg)})"
    )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Звіт 2: розклад групи
# ---------------------------------------------------------------------------

def report_group_schedule(session: Session, group_id: int) -> str:
    group_repo  = GroupRepository(session)
    lesson_repo = LessonRepository(session)

    group = group_repo.get(group_id)
    if not group:
        return f"  Групу з ID={group_id} не знайдено."

    lessons = lesson_repo.get_by_group(group_id)

    lines = [_header(f"Розклад групи: {group.name}")]
    student_names = ", ".join(s.name for s in group.students) or "—"
    lines.append(f"  Учні ({len(group.students)}): {student_names}")
    lines.append(_SEP)

    if not lessons:
        lines.append("  Занять ще немає.")
        return "\n".join(lines)

    for lesson in lessons:
        lines.append(
            f"  {lesson.datetime_}  Кімн.: {lesson.room:<6}"
            f"  {lesson.subject.name:<20}  Викл.: {lesson.teacher.name}"
        )

    lines.append(_SEP)
    lines.append(f"  Усього занять: {len(lessons)}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Звіт 3: загальна успішність по предметах
# ---------------------------------------------------------------------------

def report_school_summary(session: Session) -> str:
    subject_repo = SubjectRepository(session)
    GradeRepository(session)

    subjects = subject_repo.get_all()

    lines = [_header("Загальна успішність школи")]
    lines.append(f"  {'Предмет':<22} {'К-ть':>5}  {'Сер.бал':>8}  {'Оцінка'}")
    lines.append(_SEP)

    total_grades = 0
    total_sum    = 0.0
    has_data     = False

    for subj in subjects:
        grades = [
            g for lesson in subj.lessons for g in lesson.grades
        ]
        if not grades:
            continue
        has_data = True
        avg = sum(g.value for g in grades) / len(grades)
        total_grades += len(grades)
        total_sum    += sum(g.value for g in grades)
        lines.append(
            f"  {subj.name:<22} {len(grades):>5}  {avg:>7.1f}/12  {_grade_word(avg)}"
        )

    if not has_data:
        lines.append("  Оцінок ще немає.")
        return "\n".join(lines)

    overall_avg = total_sum / total_grades if total_grades else 0
    lines.append(_SEP)
    lines.append(
        f"  Усього оцінок: {total_grades}   "
        f"Загальний середній: {overall_avg:.1f}/12  ({_grade_word(overall_avg)})"
    )
    return "\n".join(lines)
