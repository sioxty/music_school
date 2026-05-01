"""
models.py — доменні ORM-моделі музичної школи.

ООП-концепції:
  Person        — абстрактний клас (ABC), інкапсуляція через property
  Student       — наслідує Person, перевизначає info() (поліморфізм)
  Teacher       — наслідує Person, перевизначає info() (поліморфізм)
  Subject, Group, Lesson, Grade — ORM-моделі зі зв'язками (relationship)
"""

from __future__ import annotations


from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ---------------------------------------------------------------------------
# ORM Base
# ---------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Базовий клас для всіх ORM-моделей."""
    pass


# ---------------------------------------------------------------------------
# Таблиця many-to-many: група ↔ учні
# ---------------------------------------------------------------------------

group_students = Table(
    "group_students",
    Base.metadata,
    Column("group_id",   Integer, ForeignKey("groups.id",   ondelete="CASCADE"), primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE"), primary_key=True),
)


# ---------------------------------------------------------------------------
# Абстрактний мікс-ін Person
#
# Не використовуємо ABC напряму, бо SQLAlchemy DeclarativeBase має власний
# метаклас (DeclarativeMeta), несумісний з ABCMeta.
# Натомість використовуємо __init_subclass__ для перевірки контракту
# та abstractmethod-подібну поведінку через NotImplementedError.
# ---------------------------------------------------------------------------

class Person:
    """
    Абстрактний мікс-ін для учасників школи.
    Демонструє: абстракцію, інкапсуляцію, поліморфізм.

    Підкласи зобов'язані реалізувати: name, phone (property), info().
    Перевірка відбувається при створенні підкласу (__init_subclass__).
    """

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Перевіряємо контракт лише для конкретних класів (не проміжних)
        if not getattr(cls, "__abstract_person__", False):
            required = ("info",)
            for method in required:
                if method not in cls.__dict__:
                    raise TypeError(
                        f"Клас {cls.__name__} повинен реалізувати метод '{method}()'"
                    )

    @property
    def name(self) -> str:
        raise NotImplementedError("Підклас повинен реалізувати property 'name'")

    @property
    def phone(self) -> str:
        raise NotImplementedError("Підклас повинен реалізувати property 'phone'")

    def info(self) -> str:
        """
        Повертає рядковий опис особи.
        Кожен нащадок реалізує по-своєму — поліморфізм.
        """
        raise NotImplementedError("Підклас повинен реалізувати метод 'info()'")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class Student(Base, Person):
    """
    Учень школи.
    Наслідує: Base (ORM) + Person (доменна абстракція).
    """
    __tablename__ = "students"

    id:         Mapped[int]  = mapped_column(Integer, primary_key=True, autoincrement=True)
    _name:      Mapped[str]  = mapped_column("name",  String(120), nullable=False)
    _phone:     Mapped[str]  = mapped_column("phone", String(20),  nullable=False)
    birth_date: Mapped[str]  = mapped_column(String(10), nullable=False)   # YYYY-MM-DD

    # зв'язки
    groups:  Mapped[list[Group]]  = relationship("Group",  secondary=group_students, back_populates="students")
    grades:  Mapped[list[Grade]]  = relationship("Grade",  back_populates="student", cascade="all, delete-orphan")

    def __init__(self, name: str, phone: str, birth_date: str):
        self._name  = name.strip()
        self._phone = phone.strip()
        self.birth_date = birth_date.strip()

    # --- Person interface (інкапсуляція через property) --------------------

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.strip()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value.strip()

    # --- поліморфізм -------------------------------------------------------

    def info(self) -> str:
        return (
            f"[Учень #{self.id}] {self._name} "
            f"| Народився: {self.birth_date} "
            f"| Тел.: {self._phone}"
        )


# ---------------------------------------------------------------------------
# Teacher
# ---------------------------------------------------------------------------

class Teacher(Base, Person):
    """
    Викладач школи.
    Наслідує: Base (ORM) + Person (доменна абстракція).
    """
    __tablename__ = "teachers"

    id:               Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    _name:            Mapped[str] = mapped_column("name",           String(120), nullable=False)
    _phone:           Mapped[str] = mapped_column("phone",          String(20),  nullable=False)
    _specialization:  Mapped[str] = mapped_column("specialization", String(80),  nullable=False)

    lessons: Mapped[list[Lesson]] = relationship("Lesson", back_populates="teacher")

    def __init__(self, name: str, phone: str, specialization: str):
        self._name           = name.strip()
        self._phone          = phone.strip()
        self._specialization = specialization.strip()

    # --- Person interface --------------------------------------------------

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value.strip()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value.strip()

    @property
    def specialization(self) -> str:
        return self._specialization

    @specialization.setter
    def specialization(self, value: str) -> None:
        self._specialization = value.strip()

    # --- поліморфізм -------------------------------------------------------

    def info(self) -> str:
        return (
            f"[Викладач #{self.id}] {self._name} "
            f"| Спеціалізація: {self._specialization} "
            f"| Тел.: {self._phone}"
        )


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------

class Subject(Base):
    """Музичний предмет (фортепіано, гітара, вокал…)."""
    __tablename__ = "subjects"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    lessons: Mapped[list[Lesson]] = relationship("Lesson", back_populates="subject")

    def __init__(self, name: str):
        self.name = name.strip()

    def __str__(self) -> str:
        return f"[Предмет #{self.id}] {self.name}"


# ---------------------------------------------------------------------------
# Group
# ---------------------------------------------------------------------------

class Group(Base):
    """Група учнів."""
    __tablename__ = "groups"

    id:   Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    students: Mapped[list[Student]] = relationship("Student", secondary=group_students, back_populates="groups")
    lessons:  Mapped[list[Lesson]]  = relationship("Lesson",  back_populates="group")

    def __init__(self, name: str):
        self.name = name.strip()

    def add_student(self, student: Student) -> None:
        if student not in self.students:
            self.students.append(student)

    def remove_student(self, student: Student) -> None:
        self.students = [s for s in self.students if s.id != student.id]

    def __str__(self) -> str:
        return f"[Група #{self.id}] {self.name} | Учнів: {len(self.students)}"


# ---------------------------------------------------------------------------
# Lesson
# ---------------------------------------------------------------------------

class Lesson(Base):
    """Заняття в розкладі школи."""
    __tablename__ = "lessons"

    id:         Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    datetime_:  Mapped[str] = mapped_column("datetime", String(16), nullable=False)   # YYYY-MM-DD HH:MM
    room:       Mapped[str] = mapped_column(String(20), nullable=False)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    group_id:   Mapped[int] = mapped_column(ForeignKey("groups.id"),   nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)

    teacher: Mapped[Teacher] = relationship("Teacher", back_populates="lessons")
    group:   Mapped[Group]   = relationship("Group",   back_populates="lessons")
    subject: Mapped[Subject] = relationship("Subject", back_populates="lessons")
    grades:  Mapped[list[Grade]] = relationship("Grade", back_populates="lesson", cascade="all, delete-orphan")

    def __init__(self, teacher: Teacher, group: Group, subject: Subject, datetime_: str, room: str):
        self.teacher  = teacher
        self.group    = group
        self.subject  = subject
        self.datetime_ = datetime_.strip()
        self.room      = room.strip()

    def __str__(self) -> str:
        return (
            f"[Заняття #{self.id}] {self.datetime_} | Кімн.: {self.room} "
            f"| {self.subject.name} | Викл.: {self.teacher.name} | Група: {self.group.name}"
        )


# ---------------------------------------------------------------------------
# Grade
# ---------------------------------------------------------------------------

class Grade(Base):
    """Оцінка учня за заняття (12-бальна шкала)."""
    __tablename__ = "grades"
    __table_args__ = (
        CheckConstraint("value BETWEEN 1 AND 12", name="ck_grade_value"),
    )

    id:         Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    value:      Mapped[int] = mapped_column(Integer, nullable=False)
    comment:    Mapped[str] = mapped_column(Text, default="")

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    lesson_id:  Mapped[int] = mapped_column(ForeignKey("lessons.id"),  nullable=False)

    student: Mapped[Student] = relationship("Student", back_populates="grades")
    lesson:  Mapped[Lesson]  = relationship("Lesson",  back_populates="grades")

    def __init__(self, student: Student, lesson: Lesson, value: int, comment: str = ""):
        if not (1 <= value <= 12):
            raise ValueError(f"Оцінка має бути 1–12, отримано: {value}")
        self.student = student
        self.lesson  = lesson
        self.value   = value
        self.comment = comment.strip()

    def grade_label(self) -> str:
        """Словесна оцінка за числовим значенням."""
        if self.value >= 10:
            return "відмінно"
        if self.value >= 7:
            return "добре"
        if self.value >= 4:
            return "задовільно"
        return "незадовільно"

    def __str__(self) -> str:
        comment_part = f" | {self.comment}" if self.comment else ""
        return (
            f"[Оцінка #{self.id}] {self.student.name} "
            f"| {self.lesson.subject.name} {self.lesson.datetime_} "
            f"| Бал: {self.value}/12 ({self.grade_label()}){comment_part}"
        )
