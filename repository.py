"""
repository.py — патерн Repository для музичної школи.

ООП-ієрархія:
  AbstractRepository[T]  — абстрактний generic-репозиторій
      ├── StudentRepository
      ├── TeacherRepository
      ├── SubjectRepository
      ├── GroupRepository
      ├── LessonRepository
      └── GradeRepository

Кожен репозиторій:
  - отримує Session через __init__ (dependency injection)
  - реалізує базові методи get / get_all / add / delete
  - розширює їх специфічними методами свого домену
"""

from __future__ import annotations

from abc import ABC
from typing import Generic, Optional, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import Grade, Group, Lesson, Student, Subject, Teacher

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Абстрактний репозиторій
# ---------------------------------------------------------------------------

class AbstractRepository(ABC, Generic[T]):
    """
    Універсальний generic-репозиторій.
    Забезпечує CRUD-логіку та опціональний порядок сортування.
    """

    model: Type[T]
    default_order_by: tuple = ()

    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, entity_id: int) -> Optional[T]:
        return self._session.get(self.model, entity_id)

    def get_all(self) -> list[T]:
        stmt = select(self.model)
        if self.default_order_by:
            stmt = stmt.order_by(*self.default_order_by)
        return self._scalar_list(stmt)

    def add(self, entity: T) -> T:
        self._session.add(entity)
        self._session.flush()
        return entity

    def delete(self, entity_id: int) -> bool:
        entity = self.get(entity_id)
        if not entity:
            return False
        self._session.delete(entity)
        return True

    def _scalar_list(self, stmt) -> list[T]:
        return list(self._session.execute(stmt).scalars())


# ---------------------------------------------------------------------------
# StudentRepository
# ---------------------------------------------------------------------------

class StudentRepository(AbstractRepository[Student]):
    """Репозиторій для роботи з учнями."""

    model = Student
    default_order_by = (Student._name,)

    def get_by_group(self, group_id: int) -> list[Student]:
        return self._scalar_list(
            select(self.model)
            .join(self.model.groups)
            .where(Group.id == group_id)
            .order_by(self.model._name)
        )


# ---------------------------------------------------------------------------
# TeacherRepository
# ---------------------------------------------------------------------------

class TeacherRepository(AbstractRepository[Teacher]):
    """Репозиторій для роботи з викладачами."""

    model = Teacher
    default_order_by = (Teacher._name,)

    def get_by_specialization(self, specialization: str) -> list[Teacher]:
        return self._scalar_list(
            select(self.model)
            .where(self.model._specialization.ilike(f"%{specialization}%"))
        )


# ---------------------------------------------------------------------------
# SubjectRepository
# ---------------------------------------------------------------------------

class SubjectRepository(AbstractRepository[Subject]):
    """Репозиторій для роботи з предметами."""

    model = Subject
    default_order_by = (Subject.name,)


# ---------------------------------------------------------------------------
# GroupRepository
# ---------------------------------------------------------------------------

class GroupRepository(AbstractRepository[Group]):
    """Репозиторій для роботи з групами."""

    model = Group
    default_order_by = (Group.name,)

    def add_student(self, group: Group, student: Student) -> None:
        group.add_student(student)
        self._session.flush()

    def remove_student(self, group: Group, student: Student) -> None:
        group.remove_student(student)
        self._session.flush()


# ---------------------------------------------------------------------------
# LessonRepository
# ---------------------------------------------------------------------------

class LessonRepository(AbstractRepository[Lesson]):
    """Репозиторій для роботи із заняттями."""

    model = Lesson
    default_order_by = (Lesson.datetime_,)

    def get_by_group(self, group_id: int) -> list[Lesson]:
        return self._scalar_list(
            select(self.model)
            .where(self.model.group_id == group_id)
            .order_by(self.model.datetime_)
        )

    def get_by_teacher(self, teacher_id: int) -> list[Lesson]:
        return self._scalar_list(
            select(self.model)
            .where(self.model.teacher_id == teacher_id)
            .order_by(self.model.datetime_)
        )


# ---------------------------------------------------------------------------
# GradeRepository
# ---------------------------------------------------------------------------

class GradeRepository(AbstractRepository[Grade]):
    """Репозиторій для роботи з оцінками."""

    model = Grade

    def get_by_student(self, student_id: int) -> list[Grade]:
        return self._scalar_list(
            select(self.model)
            .where(self.model.student_id == student_id)
            .order_by(self.model.lesson_id)
        )

    def get_by_lesson(self, lesson_id: int) -> list[Grade]:
        return self._scalar_list(
            select(self.model)
            .where(self.model.lesson_id == lesson_id)
            .order_by(self.model.student_id)
        )

    def average_by_student(self, student_id: int) -> Optional[float]:
        result = self._session.execute(
            select(func.avg(self.model.value)).where(self.model.student_id == student_id)
        ).scalar()
        return float(result) if result is not None else None

    def average_by_subject(self, subject_id: int) -> Optional[float]:
        result = self._session.execute(
            select(func.avg(self.model.value))
            .join(self.model.lesson)
            .where(Lesson.subject_id == subject_id)
        ).scalar()
        return float(result) if result is not None else None
