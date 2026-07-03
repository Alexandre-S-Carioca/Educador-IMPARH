from ..base import Base
from .user import User, UserRole
from .course import Course, Module, Unit, Topic
from .content import Question, Flashcard, Example
from .gamification import UserProgress, QuestionAttempt
from .activity_log import ActivityLog

# This is necessary so that Alembic sees all models.
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Course",
    "Module",
    "Unit",
    "Topic",
    "Question",
    "Flashcard",
    "Example",
    "ActivityLog"
]
