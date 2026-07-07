import uuid
import enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Enum
from ..base import Base, TimestampMixin
from .user import UserLevel


class ClassRoom(Base, TimestampMixin):
    """Representa uma turma criada por um professor."""
    __tablename__ = "classrooms"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[UserLevel] = mapped_column(Enum(UserLevel), nullable=False)
    series: Mapped[int] = mapped_column(Integer, nullable=False)  # ex: 6, 7, 8, 9, 1, 2, 3

    # Relacionamentos
    teacher: Mapped["User"] = relationship("User", back_populates="teacher_classrooms", foreign_keys=[teacher_id])
    students: Mapped[List["User"]] = relationship("User", back_populates="classroom", foreign_keys="[User.classroom_id]")
    assignments: Mapped[List["Assignment"]] = relationship("Assignment", back_populates="classroom", cascade="all, delete-orphan")
