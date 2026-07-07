import uuid
import enum
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey
from ..base import Base, TimestampMixin


class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"


class UserLevel(str, enum.Enum):
    FUNDAMENTAL_I = "FUNDAMENTAL_I"
    FUNDAMENTAL_II = "FUNDAMENTAL_II"
    HIGH_SCHOOL = "HIGH_SCHOOL"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    
    # Novos campos v2.0
    level: Mapped[Optional[UserLevel]] = mapped_column(Enum(UserLevel), nullable=True)
    classroom_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("classrooms.id", ondelete="SET NULL"), nullable=True)
    
    # Relacionamentos
    progress: Mapped["UserProgress"] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    classroom: Mapped[Optional["ClassRoom"]] = relationship(back_populates="students", foreign_keys=[classroom_id])
    
    # Um professor possui várias turmas (classrooms)
    teacher_classrooms: Mapped[List["ClassRoom"]] = relationship(
        "ClassRoom",
        back_populates="teacher",
        foreign_keys="[ClassRoom.teacher_id]"
    )
    
    essays: Mapped[List["StudentEssay"]] = relationship("StudentEssay", back_populates="student", cascade="all, delete-orphan")
    submissions: Mapped[List["StudentSubmission"]] = relationship("StudentSubmission", back_populates="student", cascade="all, delete-orphan")
