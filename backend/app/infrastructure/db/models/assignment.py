import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, JSON, DateTime
from ..base import Base, TimestampMixin


class Assignment(Base, TimestampMixin):
    """Representa uma tarefa criada por um professor para uma turma."""
    __tablename__ = "assignments"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    teacher_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    classroom_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("classrooms.id", ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # Tipo: "essay" | "quiz" | "exercise"
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="essay")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    # Critérios de avaliação em formato JSON (ex: {"criatividade": 3, "clareza": 2})
    rubric: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relacionamentos
    classroom: Mapped["ClassRoom"] = relationship("ClassRoom", back_populates="assignments")
    teacher: Mapped["User"] = relationship("User", foreign_keys=[teacher_id])
    submissions: Mapped[List["StudentSubmission"]] = relationship("StudentSubmission", back_populates="assignment", cascade="all, delete-orphan")
    essays: Mapped[List["StudentEssay"]] = relationship("StudentEssay", back_populates="assignment", cascade="all, delete-orphan")
