from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api import (
    courses_router,
    modules_router,
    units_router,
    topics_router,
    global_topics_router,
    questions_router,
    progress_router,
    ai_router,
    flashcards_router,
    activity_logs_router,
    classrooms_router,
    assignments_router,
    essays_router,
    wiki_router,
    audio_router,
    youtube_router,
    library_router
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses_router, prefix="/api/v1")
app.include_router(modules_router, prefix="/api/v1")
app.include_router(units_router, prefix="/api/v1")
app.include_router(topics_router, prefix="/api/v1")
app.include_router(global_topics_router, prefix="/api/v1")
app.include_router(questions_router, prefix="/api/v1")
app.include_router(progress_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")
app.include_router(flashcards_router, prefix="/api/v1")
app.include_router(activity_logs_router, prefix="/api/v1")
app.include_router(classrooms_router, prefix="/api/v1")
app.include_router(assignments_router, prefix="/api/v1")
app.include_router(essays_router, prefix="/api/v1")
app.include_router(wiki_router, prefix="/api/v1")
app.include_router(audio_router, prefix="/api/v1")
app.include_router(youtube_router, prefix="/api/v1")
app.include_router(library_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Educador API is running"}
