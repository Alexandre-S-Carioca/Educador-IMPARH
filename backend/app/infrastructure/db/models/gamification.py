import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean
from ..base import Base, TimestampMixin

class UserProgress(Base, TimestampMixin):
    __tablename__ = "user_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    total_xp: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    
    user: Mapped["User"] = relationship(back_populates="progress")

class QuestionAttempt(Base, TimestampMixin):
    __tablename__ = "question_attempts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    xp_awarded: Mapped[int] = mapped_column(Integer, default=0)
    
    user: Mapped["User"] = relationship()
    question: Mapped["Question"] = relationship()
