import uuid
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Float, Integer, ForeignKey, DateTime
from ..base import Base, TimestampMixin


class StudentEssay(Base, TimestampMixin):
    """Representa uma redação submetida por um aluno."""
    __tablename__ = "student_essays"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Opcional: pode ser uma redação de treino livre (sem tarefa associada)
    assignment_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("assignments.id", ondelete="SET NULL"), nullable=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)

    # Notas e feedbacks
    grade: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # 0 a 10
    ai_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Gerado pelo Groq
    teacher_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Escrito pelo professor

    # Status: "draft" | "submitted" | "reviewed" | "graded"
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft")

    # Relacionamentos
    student: Mapped["User"] = relationship("User", back_populates="essays")
    assignment: Mapped[Optional["Assignment"]] = relationship("Assignment", back_populates="essays")


class StudentSubmission(Base, TimestampMixin):
    """Representa a submissão de uma tarefa (quiz/exercício) por um aluno."""
    __tablename__ = "student_submissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    assignment_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    grade: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relacionamentos
    assignment: Mapped["Assignment"] = relationship("Assignment", back_populates="submissions")
    student: Mapped["User"] = relationship("User", back_populates="submissions")
