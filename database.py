"""
database.py — налаштування SQLAlchemy 2.0.

Відповідає виключно за:
  - створення engine
  - фабрику Session
  - ініціалізацію схеми БД
"""

from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base

_DB_PATH = Path(__file__).parent / "school.db"
_ENGINE  = create_engine(
    f"sqlite:///{_DB_PATH}",
    echo=False,
    connect_args={"check_same_thread": False},
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=_ENGINE,
    expire_on_commit=False,
)


def init_db() -> None:
    """Створює всі таблиці, якщо їх ще немає."""
    Base.metadata.create_all(_ENGINE)


def seed_demo_data() -> None:
    """Додає демонстраційні дані до бази, якщо таблиці порожні."""
    from sqlalchemy import select
    from models import Grade, Group, Lesson, Student, Subject, Teacher

    with get_session() as session:
        existing_student = session.execute(select(Student)).scalars().first()
        if existing_student:
            return

        teacher_1 = Teacher("Olena Petrenko", "+380501111111", "Piano")
        teacher_2 = Teacher("Ivan Kovalenko", "+380502222222", "Guitar")
        teacher_3 = Teacher("Kateryna Sydorenko", "+380503333333", "Voice")

        subject_1 = Subject("Piano")
        subject_2 = Subject("Guitar")
        subject_3 = Subject("Music Theory")

        group_1 = Group("Junior Ensemble")
        group_2 = Group("Advanced Quartet")

        student_1 = Student("Alice Ivanova", "+380504444444", "2008-07-12")
        student_2 = Student("Bohdan Shevchenko", "+380505555555", "2007-10-04")
        student_3 = Student("Maria Kovalska", "+380506666666", "2009-02-28")

        group_1.add_student(student_1)
        group_1.add_student(student_2)
        group_2.add_student(student_3)

        lesson_1 = Lesson(teacher_1, group_1, subject_1, "2026-05-10 15:00", "101")
        lesson_2 = Lesson(teacher_2, group_1, subject_2, "2026-05-11 16:30", "102")
        lesson_3 = Lesson(teacher_3, group_2, subject_3, "2026-05-12 14:00", "103")

        grade_1 = Grade(student_1, lesson_1, 11, "Excellent performance")
        grade_2 = Grade(student_2, lesson_2, 9, "Very good progress")
        grade_3 = Grade(student_3, lesson_3, 10, "Great participation")

        session.add_all([
            teacher_1,
            teacher_2,
            teacher_3,
            subject_1,
            subject_2,
            subject_3,
            group_1,
            group_2,
            student_1,
            student_2,
            student_3,
            lesson_1,
            lesson_2,
            lesson_3,
            grade_1,
            grade_2,
            grade_3,
        ])
        session.flush()


@contextmanager
def get_session():
    """Контекстний менеджер сесії з автоматичним commit/rollback."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
