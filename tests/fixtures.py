from __future__ import annotations

from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from models import Base, Grade, Group, Lesson, Student, Subject, Teacher

TEST_DATABASE_URL = "sqlite:///:memory:"


def create_test_engine() -> Any:
    return create_engine(TEST_DATABASE_URL, echo=False, future=True)


def create_test_session(engine: Any | None = None) -> Session:
    if engine is None:
        engine = create_test_engine()
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)
    return SessionLocal()


def create_student(name: str = "Alice", phone: str = "+380501234567", birth_date: str = "2005-05-15") -> Student:
    return Student(name, phone, birth_date)


def create_teacher(name: str = "Olena", phone: str = "+380671234567", specialization: str = "Piano") -> Teacher:
    return Teacher(name, phone, specialization)


def create_subject(name: str = "Piano") -> Subject:
    return Subject(name)


def create_group(name: str = "Junior Ensemble") -> Group:
    return Group(name)


def create_lesson(teacher: Teacher, group: Group, subject: Subject, datetime_: str = "2026-05-01 16:00", room: str = "101") -> Lesson:
    return Lesson(teacher, group, subject, datetime_, room)


def create_grade(student: Student, lesson: Lesson, value: int = 11, comment: str = "Very good") -> Grade:
    return Grade(student, lesson, value, comment)


def populate_sample_school(session: Session) -> dict[str, Any]:
    teacher = create_teacher()
    subject = create_subject()
    group = create_group()
    student = create_student()
    lesson = create_lesson(teacher, group, subject)
    grade = create_grade(student, lesson)

    session.add_all([teacher, subject, group, student, lesson, grade])
    session.flush()
    session.commit()

    return {
        "teacher": teacher,
        "subject": subject,
        "group": group,
        "student": student,
        "lesson": lesson,
        "grade": grade,
    }
