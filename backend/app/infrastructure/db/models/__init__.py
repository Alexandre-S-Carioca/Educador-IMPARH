from ..base import Base
from .user import User, UserRole, UserLevel
from .course import Course, Module, Unit, Topic
from .content import Question, Flashcard, Example, AudioContent
from .gamification import UserProgress, QuestionAttempt
from .activity_log import ActivityLog
from .classroom import ClassRoom
from .assignment import Assignment
from .essay import StudentEssay, StudentSubmission

# This is necessary so that Alembic sees all models.
__all__ = [
    "Base",
    "User",
    "UserRole",
    "UserLevel",
    "Course",
    "Module",
    "Unit",
    "Topic",
    "Question",
    "Flashcard",
    "Example",
    "AudioContent",
    "ActivityLog",
    "UserProgress",
    "QuestionAttempt",
    "ClassRoom",
    "Assignment",
    "StudentEssay",
    "StudentSubmission",
]
