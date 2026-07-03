from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import uuid
from typing import List

from ..infrastructure.db.session import get_db
from ..infrastructure.repositories.flashcard_repo import FlashcardRepository
from ..domain.schemas import FlashcardResponse, FlashcardBase

router = APIRouter(prefix="/topics/{topic_id}/flashcards", tags=["Flashcards"])

@router.post("/", response_model=FlashcardResponse)
def create_flashcard(topic_id: uuid.UUID, flashcard_in: FlashcardBase, db: Session = Depends(get_db)):
    repo = FlashcardRepository(db)
    return repo.create(topic_id, flashcard_in)

@router.get("/", response_model=List[FlashcardResponse])
def get_flashcards_by_topic(topic_id: uuid.UUID, db: Session = Depends(get_db)):
    repo = FlashcardRepository(db)
    return repo.get_by_topic(topic_id)
