from .courses import router as courses_router
from .modules import router as modules_router
from .units import router as units_router
from .topics import router as topics_router, global_router as global_topics_router
from .questions import router as questions_router
from .progress import router as progress_router
from .ai import router as ai_router
from .flashcards import router as flashcards_router
from .activity_logs import router as activity_logs_router

__all__ = ["courses_router", "modules_router", "units_router", "topics_router", "global_topics_router", "questions_router", "progress_router", "ai_router", "flashcards_router", "activity_logs_router"]
