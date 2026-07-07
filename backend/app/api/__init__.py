from .courses import router as courses_router
from .modules import router as modules_router
from .units import router as units_router
from .topics import router as topics_router, global_router as global_topics_router
from .questions import router as questions_router
from .progress import router as progress_router
from .ai import router as ai_router
from .flashcards import router as flashcards_router
from .activity_logs import router as activity_logs_router
from .classrooms import router as classrooms_router
from .assignments import router as assignments_router
from .essays import router as essays_router
from .wiki import router as wiki_router
from .audio import router as audio_router
from .youtube import router as youtube_router
from .library import router as library_router

__all__ = [
    "courses_router",
    "modules_router",
    "units_router",
    "topics_router",
    "global_topics_router",
    "questions_router",
    "progress_router",
    "ai_router",
    "flashcards_router",
    "activity_logs_router",
    "classrooms_router",
    "assignments_router",
    "essays_router",
    "wiki_router",
    "audio_router",
    "youtube_router",
    "library_router"
]
