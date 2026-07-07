import uuid
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text, JSON, Boolean
from ..base import Base, TimestampMixin

class Question(Base, TimestampMixin):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    
    topic: Mapped["Topic"] = relationship(back_populates="questions")
    
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(Text, nullable=False)
    option_b: Mapped[str] = mapped_column(Text, nullable=False)
    option_c: Mapped[str] = mapped_column(Text, nullable=False)
    option_d: Mapped[str] = mapped_column(Text, nullable=False)
    correct_option: Mapped[str] = mapped_column(String(1), nullable=False) # A, B, C, D
    
    justification_correct: Mapped[str] = mapped_column(Text, nullable=False)
    justification_incorrect: Mapped[str] = mapped_column(Text, nullable=False)
    
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    subsubject: Mapped[str] = mapped_column(String(255), nullable=False)
    board: Mapped[str] = mapped_column(String(255), default="IMPARH")
    keywords: Mapped[dict] = mapped_column(JSON, nullable=True)

class Flashcard(Base, TimestampMixin):
    __tablename__ = "flashcards"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    
    topic: Mapped["Topic"] = relationship(back_populates="flashcards")
    
    front: Mapped[str] = mapped_column(Text, nullable=False)
    back: Mapped[str] = mapped_column(Text, nullable=False)

class Example(Base, TimestampMixin):
    __tablename__ = "examples"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    
    topic: Mapped["Topic"] = relationship(back_populates="examples")
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_commented: Mapped[bool] = mapped_column(Boolean, default=False)


class AudioContent(Base, TimestampMixin):
    """Conteúdo de áudio para pronúncia e fonética de palavras/frases."""
    __tablename__ = "audio_contents"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)

    topic: Mapped["Topic"] = relationship(back_populates="audio_contents")

    word_or_phrase: Mapped[str] = mapped_column(String(255), nullable=False)
    audio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ipa_phonetic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # ex: /\u02c8pa.la.vra/
    language_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # ex: "fundamental_ii"
